#!/usr/bin/env python3
"""
🔍 MongoDB Database Analyzer for PromptForge
Connects to local MongoDB and extracts complete database structure
"""

import pymongo
import json
from datetime import datetime
from bson import ObjectId
import os

class MongoDBAnalyzer:
    def __init__(self, connection_string="mongodb://localhost:27017/", db_name="promptforge"):
        """Initialize MongoDB connection"""
        self.connection_string = connection_string
        self.db_name = db_name
        self.client = None
        self.db = None
        self.analysis_results = {}
        
    def connect(self):
        """Connect to MongoDB"""
        try:
            print(f"🔌 Connecting to MongoDB: {self.connection_string}")
            self.client = pymongo.MongoClient(self.connection_string)
            self.db = self.client[self.db_name]
            
            # Test connection
            self.client.admin.command('ping')
            print(f"✅ Connected to database: {self.db_name}")
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def json_serializer(self, obj):
        """Custom JSON serializer for MongoDB objects"""
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return str(obj)
    
    def analyze_collection(self, collection_name):
        """Analyze a single collection"""
        print(f"\n📋 Analyzing collection: {collection_name}")
        
        try:
            collection = self.db[collection_name]
            
            # Get basic stats
            doc_count = collection.count_documents({})
            stats = {
                "name": collection_name,
                "document_count": doc_count,
                "indexes": list(collection.list_indexes()),
                "sample_documents": [],
                "field_analysis": {}
            }
            
            # Try to get collection stats (if available)
            try:
                if doc_count > 0:
                    db_stats = self.db.command("collStats", collection_name)
                    stats["collection_stats"] = {
                        "size": db_stats.get("size", 0),
                        "storageSize": db_stats.get("storageSize", 0),
                        "avgObjSize": db_stats.get("avgObjSize", 0)
                    }
            except:
                stats["collection_stats"] = {}
            
            # Get sample documents (up to 3)
            sample_docs = list(collection.find().limit(3))
            for doc in sample_docs:
                # Convert to JSON-serializable format
                json_doc = json.loads(json.dumps(doc, default=self.json_serializer))
                stats["sample_documents"].append(json_doc)
            
            # Analyze field structure from first document
            if sample_docs:
                first_doc = sample_docs[0]
                stats["field_analysis"] = self.analyze_document_structure(first_doc)
            
            print(f"   📊 Documents: {stats['document_count']}")
            print(f"   🔍 Indexes: {len(stats['indexes'])}")
            print(f"   📝 Sample docs: {len(stats['sample_documents'])}")
            
            return stats
            
        except Exception as e:
            print(f"   ❌ Error analyzing {collection_name}: {e}")
            return {"name": collection_name, "error": str(e)}
    
    def analyze_document_structure(self, doc, prefix=""):
        """Recursively analyze document structure"""
        structure = {}
        
        for key, value in doc.items():
            full_key = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                structure[key] = {
                    "type": "object",
                    "fields": self.analyze_document_structure(value, full_key)
                }
            elif isinstance(value, list):
                structure[key] = {
                    "type": "array",
                    "sample_length": len(value),
                    "element_type": type(value[0]).__name__ if value else "unknown"
                }
            else:
                structure[key] = {
                    "type": type(value).__name__,
                    "sample_value": str(value)[:100] if len(str(value)) > 100 else value
                }
        
        return structure
    
    def get_all_collections(self):
        """Get list of all collections"""
        try:
            collections = self.db.list_collection_names()
            print(f"📁 Found {len(collections)} collections:")
            for i, coll in enumerate(collections, 1):
                print(f"   {i:2d}. {coll}")
            return collections
        except Exception as e:
            print(f"❌ Error getting collections: {e}")
            return []
    
    def analyze_database(self):
        """Analyze complete database"""
        print(f"🔍 MONGODB DATABASE ANALYSIS")
        print(f"=" * 50)
        print(f"Database: {self.db_name}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Get all collections
        collections = self.get_all_collections()
        
        if not collections:
            print("❌ No collections found!")
            return
        
        # Analyze each collection
        self.analysis_results = {
            "database_name": self.db_name,
            "analysis_timestamp": datetime.now().isoformat(),
            "total_collections": len(collections),
            "collections": {}
        }
        
        for collection_name in collections:
            collection_analysis = self.analyze_collection(collection_name)
            self.analysis_results["collections"][collection_name] = collection_analysis
        
        return self.analysis_results
    
    def save_analysis(self, filename=None):
        """Save analysis results to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mongodb_analysis_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.analysis_results, f, indent=2, default=self.json_serializer)
            
            print(f"\n💾 Analysis saved to: {filename}")
            print(f"📄 File size: {os.path.getsize(filename):,} bytes")
            return filename
            
        except Exception as e:
            print(f"❌ Error saving analysis: {e}")
            return None
    
    def print_summary(self):
        """Print analysis summary"""
        if not self.analysis_results:
            print("❌ No analysis results available")
            return
        
        print(f"\n" + "=" * 60)
        print(f"📊 DATABASE ANALYSIS SUMMARY")
        print(f"=" * 60)
        
        total_docs = 0
        collection_summary = []
        
        for coll_name, coll_data in self.analysis_results["collections"].items():
            if "document_count" in coll_data:
                doc_count = coll_data["document_count"]
                total_docs += doc_count
                collection_summary.append((coll_name, doc_count))
        
        # Sort by document count
        collection_summary.sort(key=lambda x: x[1], reverse=True)
        
        print(f"📁 Total Collections: {self.analysis_results['total_collections']}")
        print(f"📄 Total Documents: {total_docs:,}")
        print(f"\n📋 Collections by size:")
        
        for coll_name, doc_count in collection_summary:
            bar_length = min(30, max(1, int(doc_count / max(1, total_docs) * 30)))
            bar = "█" * bar_length
            print(f"   {coll_name:<25} {doc_count:>8,} docs {bar}")
        
        print(f"\n🔍 Key Collections:")
        key_collections = ["users", "prompts", "marketplace_listings", "transactions", "analytics_events"]
        for coll_name in key_collections:
            if coll_name in self.analysis_results["collections"]:
                coll_data = self.analysis_results["collections"][coll_name]
                if "document_count" in coll_data:
                    print(f"   ✅ {coll_name}: {coll_data['document_count']:,} documents")
                else:
                    print(f"   ❌ {coll_name}: Error accessing")
            else:
                print(f"   ❓ {coll_name}: Not found")
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("🔌 MongoDB connection closed")

def main():
    """Main execution function"""
    print("🔍 PromptForge MongoDB Database Analyzer")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = MongoDBAnalyzer()
    
    try:
        # Connect to database
        if not analyzer.connect():
            return
        
        # Analyze database
        results = analyzer.analyze_database()
        
        if results:
            # Print summary
            analyzer.print_summary()
            
            # Save detailed analysis
            filename = analyzer.save_analysis()
            
            if filename:
                print(f"\n🎯 Next Steps:")
                print(f"1. Check the detailed analysis in: {filename}")
                print(f"2. Use this data to create database documentation")
                print(f"3. Update API tests based on actual schema")
        
    except KeyboardInterrupt:
        print("\n⏹️ Analysis interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        analyzer.close()

if __name__ == "__main__":
    main()
