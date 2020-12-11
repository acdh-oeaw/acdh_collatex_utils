def get_chunks(s, chunk_size, text_id):
    """
    Function to split a text, inspired by https://stackoverflow.com/questions/57023348/python-splitting-a-long-text-into-chunks-of-strings-given-character-limit/57023373

    :param s: The text to chunk
    :type s: str

    :param chunk_size: Chunk size (in characters
    :type chunk_size: int

    :param text_id: Some identifier of the text, e.g the text's file name
    :type text_id: str

    :return: yields dicts like `{"id": "example_text.txt", "chunk_nr": "001", "text": "text of chunk", "char_count": 13}`
    :rtype: dict
    """
    start = 0
    end = 0
    counter = 1
    while start + chunk_size < len(s) and end != -1:
        end = s.rfind(" ", start, start + chunk_size + 1)
        text = s[start:end].replace('\n', '')
        yield {
            "id": f"{counter:03}___{text_id}",
            "chunk_nr": f"{counter:03}",
            "text": text,
            "char_count": len(text)
        }
        counter += 1
        start = end +1
    yield {
            "id": f"{counter:03}___{text_id}",
            "chunk_nr": f"{counter:03}",
            "text": s[start:].replace('\n', ''),
            "char_count": len(s[start:])
            }
