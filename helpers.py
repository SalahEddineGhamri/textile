def soup_to_dict(soup):
  tag = soup.name
  attrs = soup.attrs
  children = []

  for child in soup.children:
    if isinstance(child, bs4.element.Tag):
      children.append(soup_to_dict(child))
    elif isinstance(child, bs4.element.NavigableString):
      children.append(str(child).strip())

  # Check if soup.string is None and return an empty string instead
  text = soup.string.strip() if soup.string else ""

  return {"tag": tag, "attrs": attrs, "text": text, "children": children}


soup_dict = soup_to_dict(soup)
with open("myscope.json", "w") as f:
  json.dump(soup_dict, f)
