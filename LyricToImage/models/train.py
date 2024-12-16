import torch
import tqdm

from sklearn.model_selection import train_test_split
from torch.optim import AdamW

def main(model):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    optimizer = AdamW(model.parameters(), lr=5e-5)
    epochs = 5
    best_loss = float('inf')
    
    dataset = load_dataset()
    train_dataset, valid_dataset = train_test_split(dataset, test_size=0.2, random_state=42)
    for epoch in range(epochs):
        
        train_loss = 0.0
        model.train()
        
        for batch in tqdm(train_dataset):
            input_ids = batch['input_ids'].to(device).squeeze()
            attention_mask = batch['attention_mask'].to(device).squeeze()
            labels = batch['label'].to(device)
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            train_loss += loss.item()

            # back propagation
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            avg_train_loss = train_loss / len(train_dataset)
            print(f"epoch: {epoch + 1}, training loss: {avg_train_loss}")
        
        # validation
        with torch.no_grad():
            
            val_loss = 0.0    
            model.eval()
            
            for batch in tqdm(valid_dataset):
            
                input_ids = batch['input_ids'].to(device).squeeze()
                attention_mask = batch['attention_mask'].to(device).squeeze()
                labels = batch['label'].to(device)
                outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
                loss = outputs.loss
                val_loss += loss.item()
                
            val_loss /= len(valid_dataset)
            print(f"epoch: {epoch + 1}, validatation loss: {val_loss:.3f}")
        
        # early stopping
        patience = 3                
        if best_loss > val_loss:
            prev_best_loss = best_loss
            best_loss = val_loss
            print(f"previous_validation_loss : {prev_best_loss}, best_validation_loss : {best_loss}")
            best_model_weights = model.state_dict()
            torch.save(best_model_weights, f'epoch{epoch}-val_loss{best_loss}.pt')
        else:
            patience -= 1
            print(f'validation loss did not decrease.')
            if patience == 0:
                break
            
        model.load_state_dict(best_model_weights)
        torch.save(best_model_weights, f'epoch{epoch}-val_loss{best_loss}-best.pt')