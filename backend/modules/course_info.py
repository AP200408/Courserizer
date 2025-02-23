import re
import os
import math
import datetime
os.chdir(r"D:\Programming\Projects\Courserizer\backend")
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import asyncio
import numpy as np
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import LLMExtractionStrategy
import json

from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_openai import ChatOpenAI
# from langchain_groq import ChatGroq

from dotenv import load_dotenv

# from typing import List, Dict
from langchain_core.pydantic_v1 import BaseModel, Field
# from langchain_core.output_parsers import JsonOutputParser

# from utils.SemanticSplitter import SemanticSplitter
# from utils.Formulas import VS, CER, ACS

def VS(R, S, NR, P):
    return (R*math.log10(S+1)*math.log10(NR+1)*(NR/S+1))/P

def CER(D, P):
    return D/P

def ACS(R, S, NR, P, D, M):
    return (R*math.log10(NR+1)/(M+1))*math.log10(S+1)*(1/(math.log10(P+10)))*(D/10)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class MonthYear(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("string required")
        if not re.fullmatch(r"(0[1-9]|1[0-2])/\d{4}", v):
            raise ValueError("Invalid month/year format. Expected MM/YYYY")
        return v

class CourseInfo(BaseModel):
    name: str = Field(..., description="Course name")
    rating: float = Field(..., description="Rating of the course")
    number_of_rating: int = Field(..., description="Number of ratings of the course")
    number_of_students: int = Field(..., description="Number of students of the course")
    price: float = Field(..., description="Price of the course")
    duration: float = Field(..., description="Price of the course")
    last_updated: MonthYear = Field(..., description="Month and year of last updated")

class Course:
    def __init__(self, groq_api_key=GROQ_API_KEY):
        self.embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        # self.llm_llama=ChatGroq(groq_api_key=groq_api_key, model="llama-3.1-8b-instant")
        # self.llm_open_ai = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)
        # self.splitter = SemanticSplitter()

    async def fetch_page_content(self, url):
        # md_generator = DefaultMarkdownGenerator(
        #     content_filter=PruningContentFilter(threshold=0.4, threshold_type="fixed")
        # )

        browser_conf = BrowserConfig(
            # browser_type="chromium",
            headless=False,
            # ignore_https_errors=True,
            java_script_enabled=True,
            # verbose=True,
            # text_mode=True,
            # light_mode=True
        )

        llm_strategy=LLMExtractionStrategy(
                        provider="openai/gpt-4o-mini", api_token=os.getenv('OPENAI_API_KEY'),
                        schema=CourseInfo.schema_json(),
                        extraction_type="schema",
                        instruction="Extract the course information for ratings, number of ratings, number of students, price, duration, and last updated in JSON. The course contents are the first set of JSON values you recieve. There must be only one JSON value with 7 parameters and nothing more",
                        # chunk_token_threshold=1000,
                        # overlap_rate=0.0,
                        input_format="markdown",
                        # apply_chunking=True,
                        # extra_args={"temperature": 0.0, "max_tokens": 800}
                    )
        
        run_conf = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            # exclude_external_links=True,
            # remove_overlay_elements=True,
            # verbose=True,
            scan_full_page=True,
            simulate_user=True,
            # exclude_social_media_links=True,
            # stream=True,
            extraction_strategy=llm_strategy
        )

        print("Fetching Page Content")
        try:
            async with AsyncWebCrawler(config=browser_conf) as crawler:
                result = await crawler.arun(
                    url=url,
                    config=run_conf,
                )
                # print(f"Page Content Fetched {result.markdown}")
            # text = result.markdown
            
            if result.success:
                data = json.loads(result.extracted_content)
                print("Extracted items:", data[0])

                # llm_strategy.show_usage()
            else:
                print("Error:", result.error_message)
                print(f"Status code: {result.status_code}")

        except Exception as e:
            raise RuntimeError(f"Crawl4AI failed to fetch page content: {e}")

        if not data:
            raise RuntimeError("Crawl4AI did not return any text content.")
        
        def months_from_now(target_month_year):
            # Get the current date
            current_date = datetime.today()
            current_month = current_date.month
            current_year = current_date.year

            # Extract target month and year
            target_month, target_year = map(int, target_month_year.split('/'))

            # Calculate difference in months
            month_difference = (target_year - current_year) * 12 + (target_month - current_month)

            return abs(month_difference)
        
        data[0]["Months_since_last_update"].append(months_from_now(data[0]["last_updated"]))
        
        print(data[0])
        
        return [data[0]]

a = Course()
async def main():
    result = await a.fetch_page_content("https://www.udemy.com/course/certified-kubernetes-administrator-with-practice-tests/?couponCode=KEEPLEARNING")
    print(result)

asyncio.run(main()) 