from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from pathlib import Path

import yaml
import json

class GuardRail:

    def __init__(self, config_path:str=None):

        if not config_path:
            config_path = Path(__file__).parent.parent / "config" / "guardrail.yml"


        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        model_path = hf_hub_download(
            repo_id=self.config["model"]["repo_id"],
            filename=self.config["model"]["filename"]
        )

        self.llm = Llama(
            model_path=model_path,
            n_gpu_layers=self.config["model"]["n_gpu_layers"],
            n_ctx=self.config["model"]["n_ctx"],
            verbose=False,
        )

        self.system_prompt = self.config["guardrail"]["system_prompt"]

    def evaluate(self, user_prompt: str):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Oceń następujący prompt: <<{user_prompt}>>"},
        ]

        outputs = self.llm.create_chat_completion(
            messages=messages,
            max_tokens=self.config["guardrail"]["max_tokens"],
            temperature=self.config["guardrail"]["temperature"],
        )
        
        generated_text = outputs["choices"][0]["message"]["content"].strip()
        start_idx = generated_text.find('{')
        end_idx = generated_text.rfind('}') + 1
        json_str = generated_text[start_idx:end_idx]
        result = json.loads(json_str)
        return result

        