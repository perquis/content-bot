from openai import OpenAI

from src import instructions, models, utils


def gpt(markdowns: list[str], extensions: str, api_key: str):
    concatenated_markdowns = ""
    rules_with_instructions = ""
    is_more_than_one = len(markdowns) > 1

    if is_more_than_one:
        rules_with_instructions = instructions.copywriter_with_more_articles

        contents = [utils.create_divider(index) + md for index, md in enumerate(markdowns)]
        concatenated_markdowns = utils.concat_content(contents)
    else:
        rules_with_instructions = instructions.copywriter
        concatenated_markdowns = markdowns[0]

    rules_with_instructions += instructions.response_with_rules

    messages = [
        {"role": "system", "content": rules_with_instructions},
        {"role": "user", "content": concatenated_markdowns},
    ]

    chatgpt = OpenAI(api_key=api_key)
    completion = chatgpt.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.5,
        response_format=models.ResponseFormat
    )

    parsed = completion.choices[0].message.parsed

    markdown_content = parsed.markdown
    
    filename = utils.get_filename(
        parsed.title, 
        extensions
    )

    return filename, markdown_content