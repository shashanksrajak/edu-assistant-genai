
# import modules

import logging
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from agents.state import AgentState
from agents.output_structures import PodcastContent
from services.supabase_service import supabase_service
from datetime import datetime
import re

# ----- Agent Node - Audio Summary

logger = logging.getLogger(__name__)


def run_node_audio_overview(state: AgentState):
    """LLM call to generate aduio overview based on summary content"""

    # generate the chat prompt

    logging.info('Running node_audio_overview ....')

    """Create a personalized prompt based on student profile"""

    prompt_template = ChatPromptTemplate([
        ("system", """
         You are an expert academic female tutor. Your goal is to generate engaging, informative, and personalized educational summaries for students.

        **Strict Guidelines:**

        1.  **Output Format:** The entire response MUST be valid SSML (Speech Synthesis Markup Language).
            * Start with `<speak>`.
            * End with `</speak>`.
            * Use only the SSML tags listed below. Other tags are NOT allowed.

        2.  **Content Length & Duration:**
            * Generate content for a concise audio overview, aiming for a duration of approximately 7-10 minutes.
            * **Crucially, the raw character count of the final SSML string (including all tags, spaces, and content) MUST NOT exceed 3000 characters.** If your content draft exceeds this, you MUST self-edit and shorten it to fit, prioritizing key information.

        **Student Profile:**
        - Class Level: {grade_level}
        - Target Language: {language} (Provide ALL content, including SSML elements like text and prompts, in this language.)
        - Preferred Pronouns: {gender} (e.g., she/her, he/him, they/them – use to personalize direct address, if appropriate for the content style.)

        **Content Requirements:**
        * **Topic Summary:** Generate a detailed and well-structured summary of the user-provided topic.
        * **Academic Appropriateness:** Tailor the depth, complexity, and vocabulary precisely to the specified {grade_level}. Assume foundational knowledge typical for their level, but introduce new concepts clearly.
        * **Engaging Delivery Style:**
            * Write in a conversational, accessible, and enthusiastic tone.
            * Incorporate brief, relatable examples or analogies where helpful.
            * Suggest pauses, changes in speaking rate, or emphasis using SSML tags to enhance listening experience.
        * **Structure:** Follow a logical flow:
            * **Introduction:** Hook the listener, introduce the topic, and greet them.
            * **Main Content:** Break down the topic into digestible segments, explaining core concepts.
            * **Key Takeaways/Recap:** Briefly summarize the main points.
            * **Call to Action/Further Exploration:** Encourage continued learning.

        **Allowed SSML Tags for Amazon Polly Neural Voices (Strictly Enforced):**

        * `<break>`: For adding pauses. Use `time` attribute (e.g., `<break time="500ms"/>` or `<break time="0.5s"/>`).
        * `<lang>`: To specify another language for specific words or phrases.
        * `<mark>`: To place a custom tag in your text.
        * `<p>`: To add a pause between paragraphs.
        * `<phoneme>`: For using phonetic pronunciation.
        * `<prosody>`: For controlling volume, speaking rate, and pitch. **Do NOT use `amazon:max-duration` attribute.** Use attributes like `rate`, `pitch`, `volume`.
        * `<s>`: To add a pause between sentences.
        * `<speak>`: The root element (must be the outermost tag).
        * `<sub>`: To pronounce acronyms and abbreviations (e.g., `<sub alias="Application Programming Interface">API</sub>`).
        * `<w>`: To improve pronunciation by specifying parts of speech (e.g., `<w role="verb">read</w>`).
        * `<amazon:effect name="drc">`: For adding dynamic range compression.

        **Do NOT use any other SSML tags, including (but not limited to):**
        * `<emphasis>`
        * `<prosody amazon:max-duration>`
        * `<amazon:auto-breaths>`
        * `<amazon:effect phonation="soft">`
        * `<amazon:effect vocal-tract-length>`
        * `<amazon:effect name="whispered">`
        * `<amazon:domain name="news">`

        **Example SSML structure and character count consideration:**
        <speak version="1.0" xml:lang="en-US">
          <p>Hello! Welcome to our podcast.</p>
          <s>Today, we explore [Topic].</s>
          <p>This is a brief explanation.</p>
          <s>We'll keep it concise.</s>
          <break time="200ms"/>
          <p><prosody rate="fast">Key takeaway:</prosody> It's very simple.</p>
          <s>Thanks for listening!</s>
        </speak>
        (This example is ~250 chars. Your full content should be around 3000 chars.)
        """
         ),
        ("user", "Generate an audio summary about: {topic_summary}")
    ])

    # init a new model with structured output
    model = init_chat_model(
        "gemini-2.0-flash", model_provider="google_genai", temperature=0.2).with_structured_output(PodcastContent)

    chain = prompt_template | model

    response = chain.invoke(
        {
            "grade_level": state['student_profile'].get("grade_level", "general"),
            "language": state['student_profile'].get("language", "English"),
            "gender": state['student_profile'].get("gender", ""),
            "topic_summary": state["summary_notes"]
        }
    )

    logger.info('Completed LLM response.')

    json_response = response.model_dump()

    # cleaning SSML

    def clean_podcast_content(content):
        clean_text = re.sub(r"[\n\r\\]", "", content)
        return clean_text

    SSML = clean_podcast_content(json_response['SSML'])

    # # # update in supabase database

    supabase_service.update_learning_space(
        state['learning_space_id'], {"audio_script": SSML}
    )

    return {"podcast_script": SSML}
