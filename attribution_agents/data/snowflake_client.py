import snowflake.connector
import json
import logging
from typing import List, Dict, Any, Optional
from ..config.settings import settings

logger = logging.getLogger(__name__)

class SnowflakeClient:
    def __init__(self):
        self.connection = snowflake.connector.connect(
            user=settings.SNOWFLAKE_USER,
            password=settings.SNOWFLAKE_PASSWORD,
            account=settings.SNOWFLAKE_ACCOUNT,
            database=settings.SNOWFLAKE_DATABASE,
            schema=settings.SNOWFLAKE_SCHEMA
        )
    
    async def get_customer_search_history(self, customer_id: str) -> List[Dict]:
        """Retrieve customer's search history for analysis"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT query_id, customer_id, query_text, query_type, funnel_stage, timestamp
            FROM search_queries 
            WHERE customer_id = %s
            ORDER BY timestamp
        """, (customer_id,))
        
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in results]
        
    async def get_search_sessions(self, customer_id: str) -> List[Dict]:
        """Get customer's search sessions"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT session_id, customer_id, start_time, end_time, total_queries, session_outcome
            FROM search_sessions 
            WHERE customer_id = %s
            ORDER BY start_time
        """, (customer_id,))
        
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in results]
        
    async def update_intent_classification(self, query_id: str, classification: Dict):
        """Update search query with LLM intent classification"""
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE search_queries 
            SET intent_classification = %s, intent_confidence = %s
            WHERE query_id = %s
        """, (str(classification), classification.get('confidence_score', 0), query_id))
        self.connection.commit()
        
    async def calculate_search_attribution(self, customer_id: str) -> Dict:
        """Calculate attribution weights for search touchpoints"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT query_id, query_text, funnel_stage, timestamp
            FROM search_queries 
            WHERE customer_id = %s
            ORDER BY timestamp
        """, (customer_id,))
        
        results = cursor.fetchall()
        return {
            "customer_id": customer_id,
            "total_queries": len(results),
            "query_data": [dict(zip([desc[0] for desc in cursor.description], row)) for row in results]
        }

    async def get_creative_performance(self, creative_id: str) -> Optional[Dict]:
        """Get performance data for a specific creative"""
        try:
            cursor = self.connection.cursor()
            
            query = """
            SELECT 
                creative_id,
                creative_name,
                creative_type,
                campaign_id,
                total_impressions,
                unique_viewers,
                avg_viewability,
                click_through_rate,
                conversion_rate,
                brand_lift_score,
                creative_metadata,
                performance_by_frequency
            FROM creative_performance
            WHERE creative_id = %s
            """
            
            cursor.execute(query, (creative_id,))
            result = cursor.fetchone()
            
            if result:
                return {
                    'creative_id': result[0],
                    'creative_name': result[1],
                    'creative_type': result[2],
                    'campaign_id': result[3],
                    'total_impressions': result[4],
                    'unique_viewers': result[5],
                    'avg_viewability': float(result[6]) if result[6] else 0.0,
                    'click_through_rate': float(result[7]) if result[7] else 0.0,
                    'conversion_rate': float(result[8]) if result[8] else 0.0,
                    'brand_lift_score': float(result[9]) if result[9] else 0.0,
                    'creative_metadata': json.loads(result[10]) if result[10] else {},
                    'performance_by_frequency': json.loads(result[11]) if result[11] else {}
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving creative performance: {str(e)}")
            return None

    async def get_creative_impressions(self, creative_id: str) -> List[Dict]:
        """Get all impressions for a specific creative"""
        try:
            cursor = self.connection.cursor()
            
            query = """
            SELECT 
                impression_id,
                customer_id,
                creative_id,
                campaign_id,
                placement_id,
                ad_format,
                viewability_score,
                view_duration_seconds,
                interaction_data,
                timestamp,
                frequency_cap_count,
                cost
            FROM ad_impressions
            WHERE creative_id = %s
            ORDER BY timestamp ASC
            """
            
            cursor.execute(query, (creative_id,))
            results = cursor.fetchall()
            
            impressions = []
            for row in results:
                impression = {
                    'impression_id': row[0],
                    'customer_id': row[1],
                    'creative_id': row[2],
                    'campaign_id': row[3],
                    'placement_id': row[4],
                    'ad_format': row[5],
                    'viewability_score': float(row[6]) if row[6] else 0.0,
                    'view_duration_seconds': row[7],
                    'interaction_data': json.loads(row[8]) if row[8] else {},
                    'timestamp': row[9].isoformat() if row[9] else None,
                    'frequency_cap_count': row[10],
                    'cost': float(row[11]) if row[11] else 0.0
                }
                impressions.append(impression)
            
            return impressions
            
        except Exception as e:
            logger.error(f"Error retrieving creative impressions: {str(e)}")
            return []

    async def get_customer_display_history(self, customer_id: str) -> List[Dict]:
        """Get customer's complete display advertising history"""
        try:
            cursor = self.connection.cursor()
            
            query = """
            SELECT 
                ai.impression_id,
                ai.customer_id,
                ai.creative_id,
                ai.campaign_id,
                ai.placement_id,
                ai.ad_format,
                ai.viewability_score,
                ai.view_duration_seconds,
                ai.interaction_data,
                ai.timestamp,
                ai.frequency_cap_count,
                ai.cost,
                -- Also get corresponding touchpoint data
                tp.touchpoint_id,
                tp.attribution_weight,
                tp.position_in_journey
            FROM ad_impressions ai
            LEFT JOIN touchpoints tp ON ai.impression_id = tp.touchpoint_id
            WHERE ai.customer_id = %s
            ORDER BY ai.timestamp ASC
            """
            
            cursor.execute(query, (customer_id,))
            results = cursor.fetchall()
            
            display_history = []
            for row in results:
                display_record = {
                    'impression_id': row[0],
                    'customer_id': row[1],
                    'creative_id': row[2],
                    'campaign_id': row[3],
                    'placement_id': row[4],
                    'ad_format': row[5],
                    'viewability_score': float(row[6]) if row[6] else 0.0,
                    'view_duration_seconds': row[7],
                    'interaction_data': json.loads(row[8]) if row[8] else {},
                    'timestamp': row[9].isoformat() if row[9] else None,
                    'frequency_cap_count': row[10],
                    'cost': float(row[11]) if row[11] else 0.0,
                    'touchpoint_id': row[12],
                    'current_attribution_weight': float(row[13]) if row[13] else 0.0,
                    'position_in_journey': row[14]
                }
                display_history.append(display_record)
            
            logger.info(f"Retrieved {len(display_history)} display records for customer {customer_id}")
            return display_history
            
        except Exception as e:
            logger.error(f"Error retrieving customer display history: {str(e)}")
            return []

    async def get_customer_video_interactions(self, customer_id: str) -> List[Dict]:
        """Get customer's video interaction data"""
        try:
            cursor = self.connection.cursor()
            
            query = """
            SELECT 
                interaction_id,
                customer_id,
                video_id,
                campaign_id,
                video_duration_seconds,
                completion_rate,
                quartile_completions,
                engagement_points,
                drop_off_time,
                interaction_type,
                timestamp,
                video_metadata
            FROM video_interactions
            WHERE customer_id = %s
            ORDER BY timestamp ASC
            """
            
            cursor.execute(query, (customer_id,))
            results = cursor.fetchall()
            
            video_interactions = []
            for row in results:
                interaction = {
                    'interaction_id': row[0],
                    'customer_id': row[1],
                    'video_id': row[2],
                    'campaign_id': row[3],
                    'video_duration_seconds': row[4],
                    'completion_rate': float(row[5]) if row[5] else 0.0,
                    'quartile_completions': json.loads(row[6]) if row[6] else [],
                    'engagement_points': json.loads(row[7]) if row[7] else [],
                    'drop_off_time': row[8],
                    'interaction_type': row[9],
                    'timestamp': row[10].isoformat() if row[10] else None,
                    'video_metadata': json.loads(row[11]) if row[11] else {}
                }
                video_interactions.append(interaction)
            
            logger.info(f"Retrieved {len(video_interactions)} video interactions for customer {customer_id}")
            return video_interactions
            
        except Exception as e:
            logger.error(f"Error retrieving customer video interactions: {str(e)}")
            return []

    async def get_campaign_frequency_data(self, campaign_id: str) -> List[Dict]:
        """Get campaign performance data grouped by frequency levels"""
        try:
            cursor = self.connection.cursor()
            
            query = """
            SELECT 
                frequency_cap_count,
                COUNT(*) as impression_count,
                COUNT(DISTINCT customer_id) as unique_customers,
                AVG(viewability_score) as avg_viewability,
                SUM(CASE WHEN interaction_data:interaction = 'click' THEN 1 ELSE 0 END) as clicks,
                AVG(cost) as avg_cost
            FROM ad_impressions
            WHERE campaign_id = %s
            GROUP BY frequency_cap_count
            ORDER BY frequency_cap_count
            """
            
            cursor.execute(query, (campaign_id,))
            results = cursor.fetchall()
            
            frequency_data = []
            for row in results:
                frequency_record = {
                    'frequency_level': row[0],
                    'impression_count': row[1],
                    'unique_customers': row[2],
                    'avg_viewability': float(row[3]) if row[3] else 0.0,
                    'clicks': row[4],
                    'click_through_rate': float(row[4]) / row[1] if row[1] > 0 else 0.0,
                    'avg_cost': float(row[5]) if row[5] else 0.0
                }
                frequency_data.append(frequency_record)
            
            return frequency_data
            
        except Exception as e:
            logger.error(f"Error retrieving campaign frequency data: {str(e)}")
            return []

    async def get_campaign_frequency_settings(self, campaign_id: str) -> Optional[Dict]:
        """Get current frequency capping settings for a campaign"""
        try:
            # This would typically come from a campaigns table
            # For now, return default settings
            return {
                'campaign_id': campaign_id,
                'frequency_cap': 3,
                'time_window': '24h',
                'cap_type': 'rolling'
            }
            
        except Exception as e:
            logger.error(f"Error retrieving campaign frequency settings: {str(e)}")
            return None

    async def update_creative_performance_metrics(
        self, 
        creative_id: str, 
        performance_updates: Dict[str, Any]
    ):
        """Update creative performance metrics"""
        try:
            cursor = self.connection.cursor()
            
            # Build dynamic update query based on provided metrics
            update_fields = []
            values = []
            
            if 'click_through_rate' in performance_updates:
                update_fields.append('click_through_rate = %s')
                values.append(performance_updates['click_through_rate'])
            
            if 'conversion_rate' in performance_updates:
                update_fields.append('conversion_rate = %s') 
                values.append(performance_updates['conversion_rate'])
                
            if 'brand_lift_score' in performance_updates:
                update_fields.append('brand_lift_score = %s')
                values.append(performance_updates['brand_lift_score'])
            
            if not update_fields:
                return
            
            query = f"""
            UPDATE creative_performance 
            SET {', '.join(update_fields)}, last_updated = CURRENT_TIMESTAMP()
            WHERE creative_id = %s
            """
            
            values.append(creative_id)
            cursor.execute(query, tuple(values))
            self.connection.commit()
            
            logger.info(f"Updated performance metrics for creative {creative_id}")
            
        except Exception as e:
            logger.error(f"Error updating creative performance: {str(e)}")

    async def get_cross_channel_customer_data(self, customer_id: str) -> Dict[str, Any]:
        """Get combined search and display data for cross-channel analysis"""
        try:
            # Get search data
            search_data = await self.get_customer_search_history(customer_id)
            
            # Get display data  
            display_data = await self.get_customer_display_history(customer_id)
            
            # Get video interactions
            video_data = await self.get_customer_video_interactions(customer_id)
            
            return {
                'customer_id': customer_id,
                'search_touchpoints': search_data,
                'display_touchpoints': display_data,
                'video_interactions': video_data,
                'total_touchpoints': len(search_data) + len(display_data),
                'cross_channel_available': len(search_data) > 0 and len(display_data) > 0
            }
            
        except Exception as e:
            logger.error(f"Error retrieving cross-channel data: {str(e)}")
            return {'customer_id': customer_id, 'error': str(e)}
    
    async def update_touchpoint_attribution_weight(self, touchpoint_id: str, weight: float):
        """Update touchpoint attribution weight"""
        try:
            cursor = self.connection.cursor()
            
            # Try to update existing touchpoint
            cursor.execute("""
                UPDATE touchpoints 
                SET attribution_weight = %s
                WHERE touchpoint_id = %s
            """, (weight, touchpoint_id))
            
            # If no rows affected, insert new touchpoint
            if cursor.rowcount == 0:
                cursor.execute("""
                    INSERT INTO touchpoints (touchpoint_id, attribution_weight)
                    VALUES (%s, %s)
                """, (touchpoint_id, weight))
            
            self.connection.commit()
            logger.info(f"Updated attribution weight for {touchpoint_id}: {weight}")
            
        except Exception as e:
            logger.error(f"Error updating touchpoint attribution: {str(e)}")
            # Don't fail the whole process for this
    
    async def get_conversion_details(self, conversion_id: str) -> Optional[Dict]:
        """Get conversion event details"""
        try:
            cursor = self.connection.cursor()
            
            query = """
            SELECT 
                conversion_id,
                customer_id,
                conversion_type,
                conversion_value,
                timestamp,
                attribution_touchpoints
            FROM conversions
            WHERE conversion_id = %s
            """
            
            cursor.execute(query, (conversion_id,))
            result = cursor.fetchone()
            
            if result:
                return {
                    'conversion_id': result[0],
                    'customer_id': result[1],
                    'conversion_type': result[2],
                    'conversion_value': float(result[3]) if result[3] else 0.0,
                    'timestamp': result[4].isoformat() if result[4] else None,
                    'attribution_touchpoints': json.loads(result[5]) if result[5] else []
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving conversion details: {str(e)}")
            return None