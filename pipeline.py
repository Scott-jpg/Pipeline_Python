import argparse
import json
from collections import namedtuple

PreferenceMatch = namedtuple("PreferenceMatch", ["product_name", "product_codes"])

def main(product_data: list[dict], include_tags: list[str], exclude_tags: list[str]) -> list[PreferenceMatch]:
    """
    Returns all products with atleast one include_tag, excluding those with an exclude_tags

    args:
        product_data: list[Dic[
                        name: str,
                        tags: list[str],
                        code: str
                        ]]

    return:
        NamedTuple: ("PreferenceMatch", ["product_name", "product_codes"])
    """
    # Convert tags to set for reduced lookup time
    include_tags_set = set(include_tags)
    exclude_tags_set = set(exclude_tags)
    # Dic for access speed 
    pref_dic = {}

    for product in product_data:
        # Include all products in product_data
        try:
            if product["name"] not in pref_dic:
                pref_dic[product["name"]] = PreferenceMatch(product_name=product["name"], product_codes=[])
            
            if any(tag in product["tags"] for tag in include_tags_set):

                if any(tag in product["tags"] for tag in exclude_tags_set):
                    continue

                pref_dic[product["name"]].product_codes.append(product["code"])
        except KeyError:
            continue

    return list(pref_dic.values())

if __name__ == "__main__":

    def parse_tags(tags):
        return [tag for tag in tags.split(",") if tag]

    parser = argparse.ArgumentParser(
        description="Extracts unique product names matching given tags."
    )
    parser.add_argument(
        "product_data",
        help="a JSON file containing tagged product data",
    )
    parser.add_argument(
        "--include",
        type=parse_tags,
        help="a comma-separated list of tags whose products should be included",
        default="",
    )
    parser.add_argument(
        "--exclude",
        type=parse_tags,
        help="a comma-separated list of tags whose matching products should be excluded",
        default="",
    )

    args = parser.parse_args()

    with open(args.product_data) as f:
        product_data = json.load(f)

    order_items = main(product_data, args.include, args.exclude)

    for item in order_items:
        print("%s:\n%s\n" % (item.product_name, "\n".join(item.product_codes)))
