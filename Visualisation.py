import json
import os
import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self, training_dir='training', output_dir='trainingVisuel'):
        self.training_dir = training_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def loadFile(self, filename):
        filepath = os.path.join(self.training_dir, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File {filepath} does not exist.")
        with open(filepath, 'r') as f:
            self.data = json.load(f)
        return self.data

    def displayAndSaveMatrix(self, dataset_type, index, input_matrix, output_matrix, filename_prefix):
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        axes[0].imshow(input_matrix, cmap='viridis', interpolation='nearest')
        axes[0].set_title(f"{dataset_type} input [{index}]")
        axes[1].imshow(output_matrix, cmap='viridis', interpolation='nearest')
        axes[1].set_title(f"{dataset_type} output [{index}]")
        for ax in axes:
            ax.axis('off')
        plt.tight_layout()

        save_path = os.path.join(
            self.output_dir,
            f"{filename_prefix}_{dataset_type}_{index}.png"
        )
        plt.savefig(save_path)
        plt.close()

    def generateAllVisuals(self):
        for filename in os.listdir(self.training_dir):
            if not filename.endswith('.json'):
                continue
            try:
                self.loadFile(filename)
            except Exception as e:
                print(f"Skipping {filename}: {e}")
                continue

            for dataset_type in ['train', 'test']:
                if dataset_type not in self.data:
                    continue
                for i, entry in enumerate(self.data[dataset_type]):
                    self.displayAndSaveMatrix(
                        dataset_type,
                        i,
                        entry['input'],
                        entry['output'],
                        filename_prefix=os.path.splitext(filename)[0]
                    )
