import numpy as np
import pandas as pd

def removeLetter(text: str, prob:float=0.01) -> str:
    nparr = np.frombuffer(text.encode('utf-8'), dtype=np.uint8).copy()
    mask = np.random.random(len(nparr)) > prob
    
    return nparr[mask].tobytes().decode('utf-8', 'ignore')

def changeLetter(text:str, prob:float=0.01) -> str:
    nparr = np.frombuffer(text.encode('utf-8'), dtype=np.uint8).copy()

    mask = np.random.random(len(nparr)) < prob
    indices = np.where(mask)[0]
    
    new_chars = np.random.randint(97, 123, size=len(indices), dtype=np.uint8)
    nparr[indices] = new_chars
    
    return nparr.tobytes().decode('utf-8', 'ignore')


def data_augmentation(path:str=None, remove_prob:float=0.01, change_prob:float=0.01) -> None:
    df = pd.read_csv(path)

    df_original = df.copy()
    
    df_changed = df.copy()
    df_changed["prompt"] = df_changed["prompt"].apply(lambda x: changeLetter(str(x), change_prob))
    
    df_removed = df.copy()
    df_removed["prompt"] = df_removed["prompt"].apply(lambda x: removeLetter(str(x), remove_prob))

    final_df = pd.concat([df_original, df_changed, df_removed], ignore_index=True)

    final_df = final_df.sample(frac=1).reset_index(drop=True)

    output_path = path.replace(".csv", "_augmented.csv")
    final_df.to_csv(output_path, index=False, encoding='utf-8')