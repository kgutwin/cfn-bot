import re


SERVICE_EXTRACT = re.compile(r'AWS::([^:]+)::')
def format_post(header, body, link, date, max_len=280):
    if link is None:
        link = ""

    service_hit = SERVICE_EXTRACT.search(header)
    if service_hit is not None:
        service_tag = "#" + service_hit.group(1).lower() + ' '
    else:
        service_tag = ""
        
        
    # First yield the most likely version.
    yield f"""{header}

{body}
{link} {service_tag}#cloudformation"""

    # Next, trim the body to the first sentence.
    first_sentence = body.split('. ')[0]
    if len(body) > len(first_sentence) and body[len(first_sentence)] == '.':
        first_sentence += '.'
    yield f"""{header}

{first_sentence}
{link} {service_tag}#cloudformation"""

    # Now truncate the first sentence at the most appropriate space
    chp = min(max_len - 46 - len(header) - len(service_tag), len(body) - 1)
    while body[chp] != ' ':
        chp -= 1
        if chp == 0:
            return
    first_chunk = body[:chp]
    yield f"""{header}

{first_chunk}...
{link} {service_tag}#cloudformation"""
    
