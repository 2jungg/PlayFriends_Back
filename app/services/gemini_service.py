import google.generativeai as genai
import json
import datetime
from typing import List, Dict, Any

from app.core.config import settings
from app.models.activity import ActivityModel

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def generate_realistic_schedule(self, activities: List[ActivityModel], start_time: datetime.datetime, end_time: datetime.datetime) -> List[Dict[str, Any]]:
        prompt = self._create_prompt(activities, start_time, end_time)
        try:
            response = await self.model.generate_content_async(prompt)
            
            # Extract JSON from the response text
            response_text = response.text
            json_start = response_text.find('```json')
            json_end = response_text.rfind('```')
            
            if json_start != -1 and json_end != -1:
                json_str = response_text[json_start + 7 : json_end].strip()
                schedule_data = json.loads(json_str)
                
                # Convert time strings to datetime objects
                for item in schedule_data:
                    item['start_time'] = datetime.datetime.fromisoformat(item['start_time'])
                    item['end_time'] = datetime.datetime.fromisoformat(item['end_time'])
                return schedule_data
            else:
                # Fallback or error handling if JSON is not found
                return []

        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return []

    def _create_prompt(self, activities: List[ActivityModel], start_time: datetime.datetime, end_time: datetime.datetime) -> str:
        activity_list_str = "\n".join([f"- {activity.name} (ID: {activity.id}, Category: {activity.type.value})" for activity in activities])
        
        prompt = f"""
You are an expert trip planner. Your task is to create a realistic and enjoyable schedule based on a given list of activities and a time window.

**Instructions:**
1.  Analyze the provided list of activities, considering their type (e.g., FOOD, ACTIVITY).
2.  Determine a logical sequence for these activities. For example, don't schedule two meals back-to-back.
3.  Allocate a reasonable amount of time for each activity. Consider that meals usually take about 1-1.5 hours, and other activities might take 1-2 hours.
4.  Schedule meal times around lunch and dinner hours, and plan alcoholic activities for the evening.
5.  The total schedule must fit within the given start and end times.
6.  Return the schedule as a JSON array. Each object in the array should represent a scheduled activity and must include `activity_id`, `start_time`, and `end_time` in ISO 8601 format.

**Input:**
- **Start Time:** {start_time.isoformat()}
- **End Time:** {end_time.isoformat()}
- **Activities:**
{activity_list_str}

**Output Format (JSON only):**
```json
[
  {{
    "activity_id": "...",
    "start_time": "YYYY-MM-DDTHH:MM:SS",
    "end_time": "YYYY-MM-DDTHH:MM:SS"
  }},
  ...
]
```
"""
        return prompt
