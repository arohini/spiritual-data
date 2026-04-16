from typing import Annotated
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from PyPDF2 import PdfReader
from enum import Enum
from datetime import datetime
from storage_connection import MongodbOperations
from bson.objectid import ObjectId
from opentelemetry import trace
from opentelemetry import metrics
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
mdo = MongodbOperations("ssb_library")


# Acquire a tracer
tracer = trace.get_tracer("spiritualdata.tracer")
# Acquire a meter.
meter = metrics.get_meter("spiritualdata.meter")

# Now create a counter instrument to make measurements with
hymn_counter = meter.create_counter(
    "spiritualdata.hymns",
    description="The number of spiritual hymns requested by users",
)

chapters = {
    1: "The Invocation",
    2: "The Purpose of the Narration and the Naming Ceremony",
    3: "The Consent Given to Write this Book",
    4: "The Appearance of Sai Samartha",
    5: "The Re-appearance of Sree Sai",
    6: "The Narration of the Story of Ram-janam Celebrations",
    7: "The Narration of Various Stories",
    8: "The Incarnation of Sai Samartha",
    9: "The Easiest Path (Untitled in original Marathi)",
    10: "The Greatness of Sree Sai Samartha",
    11: "The Description of Sree Sai's Greatness",
    12: "The Darshan of Ram – Sree Sant Gholap",
    13: "The Cure of Bhimaji's Tuberculosis",
    14: "Ruttonji's Meeting with Sai",
    15: "The Story of Cholkar's Sugar",
    16: "The Narration of the Knowledge of Brahman (Part 1)",
    17: "The Narration of the Knowledge of Brahman (Part 2)",
    18: "Favour that was Bestowed on Me (Part 1)",
    19: "Favour that was Bestowed on Me (Part 2)",
    20: "The Lesson of the Essence of the Ishavasya",
    21: "Bestowing Grace",
    22: "Warding Off of Untimely Death",
    23: "The Spectacle of the Leela of Guru and Disciple",
    24: "Splendid Humour",
    25: "Achieving the Devotee's Welfare by Granting Desires",
    26: "Prevention of Epilepsy and Suicide",
    27: "Bestowal of Initiation and Grace",
    28: "Narration of Visions",
    29: "Narration of Stories of Dreams",
    30: "Narration of Vows and Other Stories",
    31: "The Greatness of Darshan",
    32: "Narration of the Guru's Greatness",
    33: "The Power of the Udi",
    34: "The Greatness of Udi (Continued)",
    35: "The Erasure of Doubts and Misapprehensions",
    36: "The All-Pervasiveness of Sai and Fulfilment of Blessings",
    37: "Description of the Chavadi",
    38: "Description of the Cooking and the Vessel",
    39: "The Discourse on the Geeta and Creation of Samadhi Mandir",
    40: "The Narration of the Udyapan Story",
    41: "The Bestowal of Sai's Grace and Favour",
    42: "Leaving of the Body by Sainath (Part 1)",
    43: "Leaving of the Body by Sainath (Part 2)",
    44: "Leaving of the Body by Sainath (Part 3)",
    45: "The Greatness of the Feet of Sree Guru",
    46: "Trip to Kashi and Gaya",
    47: "Narration of Story Told by Sree Sai",
    48: "Granting of Favour to Doubting Devotee",
    49: "Testing the Saint and the Control of the Mind",
    50: "Removal of Ignorance",
    51: "A Triad of Stories of Three Devotees",
    52: "An Overall View / Summary",
    53: "Avataranika (Epitome)",
}


@app.get("/about/{author_name}")
def about_author(author_name: str):
    return {"message": f"About {author_name}"}


@app.get("/about/me")
def about_me():
    return {
        "message": "I am a digital assistant for the Shirdi Sai Baba Digital Library and Experience Journal!"
    }


@app.get("/home")
def home():
    return {
        "message": "Welcome to the Shirdi Sai Baba Digital Library and Experience Journal!"
    }


@app.get("/ssb-sc/index")
def get_ssb_index():
    return chapters


class ChapterRequest(BaseModel):
    id: int


class DivineList(str, Enum):
    sai_baba = "sai-baba"
    lord_ganesha = "lord-ganesha"
    lord_muruga = "lord-muruga"
    lord_krishna = "lord-krishna"

class JournalEntry(BaseModel):
    content: str
    author: str
    chapter_number: int
    date: datetime | None = datetime.now()
    

@app.get("/ssb-sc/chapter-name/{chapter_id}")
def get_chapter_name(chapter_id: int) -> dict:
    # Here you would typically fetch the chapter name for the given chapter_id
    # To do: from a database
    logging.info(f"Received request for chapter ID: {chapter_id}")
    with tracer.start_as_current_span("hymn_request") as hymn_span:
        chapter_name = chapters.get(chapter_id, "Chapter not found")
        result = {"chapter_id": chapter_id, "chapter_name": chapter_name}
        hymn_span.set_attribute("hymn_request_value", chapter_name)
        hymn_counter.add(1, result)
        return result


@app.get("/data-list/{supreme-list}")
def get_divine_list(supreme_list: DivineList) -> dict:
    # Here you would typically fetch the divine list for the given supreme_list
    print(f"Received request for divine list: {supreme_list}")
    if supreme_list == DivineList.sai_baba:
        return {"divine_list": "ssb-sc refers to the Shirdi Sai Baba Satcharitra, \
            which is a sacred text that narrates the life, teachings, and miracles \
                of Shirdi Sai Baba. It is a revered scripture among devotees of Sai Baba \
                    and serves as a guide for spiritual growth and devotion."}
    elif supreme_list == DivineList.lord_ganesha:
        return {
            "divine_list": "API's provide a structured way to access and interact with \
            data, allowing developers to retrieve information about Lord Ganesha's stories,\
                teachings."
        }
    elif supreme_list == DivineList.lord_muruga:
        return {"divine_list": "API's blesses us with thirupugazh data, \
            which is a collection of Tamil devotional songs dedicated to Lord Muruga."}
    elif supreme_list == DivineList.lord_krishna:
        return {"divine_list": "This API guides us through the Bhagavad Gita, \
            a sacred Hindu scripture that is part of the Indian epic Mahabharata. \
            The Bhagavad Gita is a conversation between Prince Arjuna and Lord Krishna, \
                who serves"}
    else:
        raise HTTPException(status_code=404, detail="Divine list not found")


@app.get("/ssb-sc/chapter-content/{chapter_file:path}")
def get_chapter_content(chapter_file: str, content_limit: int) -> dict:
    # Here you would typically fetch the chapter content for the given file path
    # To do: from a database or file system
    # data/ssb-sc/Sri-Sai-Satcharitra-English.pdf
    print(f"Received request for chapter file: {chapter_file}")
    full_path = chapter_file

    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found")

    if not full_path.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Not a PDF file")

    try:
        reader = PdfReader(full_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return {
            "file": chapter_file,
            "content_preview": text[:content_limit],  # return only first 500 chars
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ssb-sc/experience-journal")
def get_experience_journal_entries():
    # Here you would typically fetch all experience journal entries from a database
    try:
        entries = mdo.get_collection("experience_journal").find().sort("date", -1) 
        # Sort by date in descending order
        # Convert MongoDB documents to Json-serializable format
        entries_list = []
        for entry in entries:
            entry["_id"] = str(entry["_id"])  # Convert ObjectId to string
            entries_list.append(entry)
        if entries_list:return entries_list[0]
        else: return {"message": "No experience journal entries found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ssb-sc/experience-journal")
def create_experience_journal(
    entry: Annotated[JournalEntry, "The content of the experience journal entry"]
):
    """
    Creates a new experience journal entry.
    Args:
        entry (JournalEntry): The content of the experience journal entry.
    Returns:
        dict: A message confirming the creation of the 
        experience journal entry and its reference ID.
    """
    author = entry.author
    econtent = entry.content
    chapter_number = entry.chapter_number
    date = entry.date
    entry_ref_id = f"{author}_{date.strftime('%Y%m%d%H%M%S')}"
    data = entry.model_dump()
    data["entry_ref_id"] = entry_ref_id
    print(f"Received experience journal entry: {data}")
    try:
        mdo.insert_one("experience_journal", data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # Here you would typically save the experience journal entry to a database
    return {"message": "Experience journal entry created successfully!", 
            "entry_ref_id": entry_ref_id}


@app.get("/ssb-sc/experience-journal/{entry_id}")
def get_experience_journal_entry(
    entry_id: Annotated[int, "The ID of the experience journal entry to retrieve"],
):
    """
    Retrieves a specific experience journal entry by its entry reference ID.
    Args:
    entry_id (str): The reference ID of the experience journal entry to retrieve.
    Returns:
    dict: The content of the experience journal entry.
    """
    # Here you would typically fetch the experience journal entry from a database
    return {
        "entry_id": entry_id,
        "content": "This is the content of the experience journal entry.",
    }


@app.put("/ssb-sc/experience-journal/{entry_id}")
def update_experience_journal_entry(
    entry_ref_id: Annotated[str, "The reference ID of the experience journal entry to update"],
    entry: Annotated[str, "The updated content of the experience journal entry"],
):
    """
    Updates the experience content from the journal entry for the given entry reference ID.
    Args:    
    entry_ref_id (str): The reference ID of the experience journal entry to update.
    entry (str): The updated content of the experience journal entry.
    Returns:    
    dict: A message confirming the update of the experience journal entry.
    """
    
    update_data = {
        "content": entry,
        "date": datetime.now()
    }
    try:        
        result = mdo.get_collection("experience_journal").update_one(
            {"entry_ref_id": entry_ref_id},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Experience journal entry not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # Here you would typically update the experience journal entry in a database
    return {
        "message": "Experience journal entry updated successfully!"
    }


@app.delete("/ssb-sc/experience-journal/{object_id}")
def delete_experience_journal_entry(
    object_id: Annotated[str, "The ID of the unique reference of the document"],
):
    """Deletes the experience journal entry with the given unique reference ID.
    Args:
        object_id (str): The unique reference ID of the experience journal entry to delete.
    Returns:
        dict: A message confirming the deletion of the experience journal entry."""
    try:
        ob_id = ObjectId(object_id)
        print(f"Received request to delete experience journal entry with ID: {ob_id}")
        result = mdo.get_collection("experience_journal").delete_one({"_id": ob_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Experience journal entry not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # Here you would typically delete the experience journal entry from a database
    return {
        "message": "Experience journal entry deleted successfully!",
        "object_id": object_id,
    }
