
from datasets import load_dataset

# Hugging Face dataset repositories
DATASETS = {
    "Institutions": "Mahadih534/Institutional-Information-of-Bangladesh",
    "Hospitals": "Mahadih534/all-bangladeshi-hospitals",
    "Restaurants": "Mahadih534/Bangladeshi-Restaurant-Data"
}


def inspect_dataset(name, repository):
    print("\n" + "=" * 60)
    print(f"INSPECTING: {name}")
    print("=" * 60)

    try:
        # Load dataset from Hugging Face
        dataset = load_dataset(repository)

        # Inspect each available split
        for split_name, split_data in dataset.items():

            print(f"\nSplit: {split_name}")
            print(f"Total records: {len(split_data)}")

            print("\nColumn names:")
            print(split_data.column_names)

            print("\nData types:")
            print(split_data.features)

            print("\nFirst two records:")

            for record in split_data.select(range(min(2, len(split_data)))):
                print(record)

    except Exception as error:
        print(f"Error loading {name}: {error}")


if __name__ == "__main__":

    for name, repository in DATASETS.items():
        inspect_dataset(name, repository)
