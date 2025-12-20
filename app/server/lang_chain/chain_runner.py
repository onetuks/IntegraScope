from enum import Enum

from charset_normalizer.md import lru_cache
from jinja2 import Template
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from app.server.lang_chain import ANALYSIS_SYSTEM_PROMPT, \
  SOLUTION_SYSTEM_PROMPT, ANALYSIS_USER_PROMPT, \
  SOLUTION_USER_PROMPT
from app.server.utils.config import get_config


class AgentType(Enum):
  ANALYSIS = "ANALYSIS"
  SOLUTION = "SOLUTION"


class LangChainClient:
  def __init__(self):
    self._llm = self._build_llm()
    self._chain = self._build_chain()

  def _build_llm(self):
    config = get_config()
    if not config.google_api_key:
      raise EnvironmentError("google_api_key is required")

    return ChatGoogleGenerativeAI(
        model=config.gemini_model,
        temperature=config.temperature
    )

  def _build_chain(self):
    prompt = ChatPromptTemplate.from_messages(
        [
          ("system", "{system_prompt}"),
          ("user", "{user_prompt}")
        ]
    )
    return prompt | self._llm | JsonOutputParser()

  @staticmethod
  def _format_system_prompt(agent_type: AgentType) -> str:
    if agent_type == AgentType.ANALYSIS:
      return ANALYSIS_SYSTEM_PROMPT
    return SOLUTION_SYSTEM_PROMPT

  @staticmethod
  def _format_user_prompt(
      agent_type: AgentType,
      artifact_type: str,
      status_code: int,
      exception: str,
      log: str,
      analysis_json: str | None = None
  ) -> str:
    if agent_type == AgentType.ANALYSIS:
      return Template(ANALYSIS_USER_PROMPT).render(
          artifact_type=artifact_type, status_code=status_code,
          exception=exception, log=log)
    return Template(SOLUTION_USER_PROMPT).render(
        artifact_type=artifact_type, status_code=status_code,
        exception=exception, log=log, analysis_json=analysis_json)

  def run_chain(self,
      agent_type: AgentType,
      artifact_type: str,
      status_code: int,
      exception: str,
      log: str):
    system_prompt = self._format_system_prompt(agent_type=agent_type)
    user_prompt = self._format_user_prompt(agent_type=agent_type,
                                           artifact_type=artifact_type,
                                           status_code=status_code,
                                           exception=exception,
                                           log=log)
    return self._chain.invoke(
        {"system_prompt": system_prompt, "user_prompt": user_prompt})


@lru_cache(maxsize=1)
def get_langchain_client() -> LangChainClient:
  return LangChainClient()
