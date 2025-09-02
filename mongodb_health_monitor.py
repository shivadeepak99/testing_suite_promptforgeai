#!/usr/bin/env python3
"""
🔄 MongoDB Health Monitor for PromptForge
Continuous monitoring script for database health, performance, and growth
"""

import pymongo
import json
import time
from datetime import datetime, timedelta
from bson import ObjectId

class MongoHealthMonitor:
    def __init__(self, connection_string="mongodb://localhost:27017/", db_name="promptforge"):
        self.connection_string = connection_string
        self.db_name = db_name
        self.client = None
        self.db = None
        
    def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = pymongo.MongoClient(self.connection_string)
            self.db = self.client[self.db_name]
            self.client.admin.command('ping')
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def get_collection_health(self):
        """Get health status of all collections"""
        collections = self.db.list_collection_names()
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "total_collections": len(collections),
            "collection_stats": {}
        }
        
        total_documents = 0
        for collection_name in collections:
            try:
                collection = self.db[collection_name]
                doc_count = collection.count_documents({})
                total_documents += doc_count
                
                # Get recent activity (last 24 hours)
                yesterday = datetime.now() - timedelta(days=1)
                recent_docs = 0
                
                # Try different timestamp fields
                for field in ['created_at', 'timestamp', 'updated_at']:
                    try:
                        recent_docs = collection.count_documents({
                            field: {"$gte": yesterday}
                        })
                        if recent_docs > 0:
                            break
                    except:
                        continue
                
                health_report["collection_stats"][collection_name] = {
                    "total_documents": doc_count,
                    "recent_activity": recent_docs,
                    "status": "healthy" if doc_count >= 0 else "error"
                }
                
            except Exception as e:
                health_report["collection_stats"][collection_name] = {
                    "error": str(e),
                    "status": "error"
                }
        
        health_report["total_documents"] = total_documents
        return health_report
    
    def check_index_performance(self):
        """Check index usage and performance"""
        collections = ["users", "prompts", "auth_logs", "usage", "transactions"]
        index_report = {}
        
        for collection_name in collections:
            try:
                collection = self.db[collection_name]
                if collection.count_documents({}) > 0:
                    # Get index stats (if available)
                    try:
                        stats = self.db.command("collStats", collection_name, indexDetails=True)
                        index_report[collection_name] = {
                            "total_indexes": len(list(collection.list_indexes())),
                            "collection_size": stats.get("size", 0),
                            "index_size": stats.get("totalIndexSize", 0)
                        }
                    except:
                        index_report[collection_name] = {
                            "total_indexes": len(list(collection.list_indexes())),
                            "note": "Detailed stats unavailable"
                        }
            except Exception as e:
                index_report[collection_name] = {"error": str(e)}
        
        return index_report
    
    def get_user_activity_summary(self):
        """Get user activity summary"""
        try:
            users_collection = self.db["users"]
            auth_logs_collection = self.db["auth_logs"]
            
            # Active users
            total_users = users_collection.count_documents({})
            active_users = users_collection.count_documents({
                "account_status": "active"
            })
            
            # Recent logins (last 7 days)
            week_ago = datetime.now() - timedelta(days=7)
            recent_logins = 0
            
            try:
                recent_logins = auth_logs_collection.count_documents({
                    "event_type": "login",
                    "timestamp": {"$gte": week_ago}
                })
            except:
                # Try different field names
                for field in ['created_at', 'timestamp']:
                    try:
                        recent_logins = auth_logs_collection.count_documents({
                            "event_type": "login",
                            field: {"$gte": week_ago}
                        })
                        break
                    except:
                        continue
            
            return {
                "total_users": total_users,
                "active_users": active_users,
                "recent_logins_7d": recent_logins,
                "activity_rate": f"{(recent_logins/max(1,total_users)*100):.1f}%"
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def get_business_metrics(self):
        """Get key business metrics"""
        try:
            prompts = self.db["prompts"].count_documents({})
            ideas = self.db["ideas"].count_documents({})
            transactions = self.db["transactions"].count_documents({})
            
            # Check for recent business activity
            yesterday = datetime.now() - timedelta(days=1)
            recent_prompts = 0
            recent_ideas = 0
            
            try:
                recent_prompts = self.db["prompts"].count_documents({
                    "created_at": {"$gte": yesterday}
                })
            except:
                pass
            
            try:
                recent_ideas = self.db["ideas"].count_documents({
                    "created_at": {"$gte": yesterday}
                })
            except:
                pass
            
            return {
                "total_prompts": prompts,
                "total_ideas": ideas,
                "total_transactions": transactions,
                "recent_prompts_24h": recent_prompts,
                "recent_ideas_24h": recent_ideas
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def print_health_dashboard(self):
        """Print a comprehensive health dashboard"""
        print("🔍 PromptForge Database Health Monitor")
        print("=" * 60)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🗄️  Database: {self.db_name}")
        
        # Collection Health
        print("\n📊 COLLECTION HEALTH")
        print("-" * 40)
        health = self.get_collection_health()
        
        active_collections = [name for name, stats in health["collection_stats"].items() 
                            if stats.get("total_documents", 0) > 0]
        empty_collections = [name for name, stats in health["collection_stats"].items() 
                           if stats.get("total_documents", 0) == 0]
        
        print(f"📁 Total Collections: {health['total_collections']}")
        print(f"📄 Total Documents: {health['total_documents']:,}")
        print(f"🟢 Active Collections: {len(active_collections)}")
        print(f"⭐ Ready Collections: {len(empty_collections)}")
        
        print(f"\n📈 ACTIVE COLLECTIONS:")
        for collection_name in sorted(active_collections):
            stats = health["collection_stats"][collection_name]
            docs = stats.get("total_documents", 0)
            recent = stats.get("recent_activity", 0)
            activity_indicator = "🔥" if recent > 0 else "📊"
            print(f"   {activity_indicator} {collection_name:<20} {docs:>6,} docs ({recent} recent)")
        
        # User Activity
        print(f"\n👥 USER ACTIVITY")
        print("-" * 40)
        user_stats = self.get_user_activity_summary()
        if "error" not in user_stats:
            print(f"👤 Total Users: {user_stats['total_users']}")
            print(f"✅ Active Users: {user_stats['active_users']}")
            print(f"🔄 Recent Logins (7d): {user_stats['recent_logins_7d']}")
            print(f"📈 Activity Rate: {user_stats['activity_rate']}")
        else:
            print(f"❌ Error: {user_stats['error']}")
        
        # Business Metrics
        print(f"\n💼 BUSINESS METRICS")
        print("-" * 40)
        business = self.get_business_metrics()
        if "error" not in business:
            print(f"📝 Total Prompts: {business['total_prompts']}")
            print(f"💡 Total Ideas: {business['total_ideas']}")
            print(f"💳 Total Transactions: {business['total_transactions']}")
            print(f"🆕 Recent Prompts (24h): {business['recent_prompts_24h']}")
            print(f"🆕 Recent Ideas (24h): {business['recent_ideas_24h']}")
        else:
            print(f"❌ Error: {business['error']}")
        
        # Index Performance
        print(f"\n🔍 INDEX PERFORMANCE")
        print("-" * 40)
        index_stats = self.check_index_performance()
        for collection_name, stats in index_stats.items():
            if "error" not in stats:
                indexes = stats.get("total_indexes", 0)
                size = stats.get("collection_size", 0)
                print(f"   📊 {collection_name:<15} {indexes:>2} indexes, {size:>8,} bytes")
            else:
                print(f"   ❌ {collection_name:<15} Error: {stats['error'][:30]}")
        
        print(f"\n" + "=" * 60)
    
    def continuous_monitor(self, interval_seconds=300):
        """Run continuous monitoring"""
        print(f"🔄 Starting continuous monitoring (every {interval_seconds}s)")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                self.print_health_dashboard()
                print(f"\n⏰ Next check in {interval_seconds} seconds...")
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print(f"\n⏹️  Monitoring stopped by user")
    
    def close(self):
        if self.client:
            self.client.close()

def main():
    monitor = MongoHealthMonitor()
    
    if not monitor.connect():
        return
    
    try:
        # Single health check
        monitor.print_health_dashboard()
        
        # Ask if user wants continuous monitoring
        response = input(f"\n🔄 Start continuous monitoring? (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            monitor.continuous_monitor()
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        monitor.close()

if __name__ == "__main__":
    main()
