## import the PyTorch library
import torch

## Import the time library
import time

## Calculate the start time
start = time.time()

import math
from random import*
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, deque
from itertools import count

import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F



# set up matplotlib
is_ipython = 'inline' in matplotlib.get_backend()
if is_ipython:
    from IPython import display

plt.ion()



device = torch.device("cpu") ## you cannot use GPU because Pytorch does not support the Intel GPU of this Macbook


# seed = 42
# random.seed(seed)
# torch.manual_seed(seed)
# if torch.cuda.is_available():
#     torch.cuda.manual_seed(seed)


Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))




class DQN(nn.Module):

    def __init__(self, n_observations, n_actions):
        super(DQN, self).__init__()
        
        ## CONSIDER CHANGING !!!
        self.layer1 = nn.Linear(n_observations, 128)
        self.layer2 = nn.Linear(128, 128) 
        self.layer3 = nn.Linear(128, n_actions)

    def forward(self, x):
        x = F.relu(self.layer1(x)) ## applied between layers to create non-linearity and make the AI leanr complex patterns 
        x = F.relu(self.layer2(x))
        return self.layer3(x)
    
#####################

# LR is the learning rate of the ``AdamW`` optimizer

GAMMA = 0.99 ## at "0" the agent considers only immediate rewards, "0.5" future rewards counts half as much as immediate, "0,99" almost as important

EPS_START = 0.9 ## how much the agent explores 
EPS_END = 0.01

EPS_DECAY = 2500 ## the higher is the number, the slower is the decay of EPS
## Consider lowering!!


LR = 1e-3 #3e-4 ## Learning rate, CONSIDER CHANGING



n_actions = 2 ##output number

n_observations = 2 ## number of input


policy_net = DQN(n_observations, n_actions).to(device)

optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)



steps_done = 0

#### Q-network 
def select_action(state): ## Greedy policy!?
    
    global steps_done
    sample = random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * \
        math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1
    
    
    if sample > eps_threshold: ## Greedy policy?
        with torch.no_grad():
            # t.max(1) will return the largest column value of each row.
            # second column on max result is index of where max element was
            # found, so we pick action with the larger expected reward.
            return policy_net(state).max(1).indices.view(1, 1)
    else:
        ## random choice
        return torch.tensor([[randint(0, n_actions-1)]], device=device, dtype=torch.long)


episode_durations = []


###### FOR GRAPH AND VISUALISATION
def plot_durations(show_result=False):
    plt.figure(1)
    durations_t = torch.tensor(episode_durations, dtype=torch.float)
    if show_result:
        plt.title('Result')
    else:
        plt.clf()
        plt.title('Training...')
    plt.xlabel('Episode')
    plt.ylabel('Duration')
    plt.plot(durations_t.numpy())
    # Take 100 episode averages and plot them too
    if len(durations_t) >= 25:
        means = durations_t.unfold(0, 25, 1).mean(1).view(-1)
        means = torch.cat((torch.zeros(24), means))
        plt.plot(means.numpy())
    
    plt.pause(0.001)  # pause a bit so that plots are updated
    if is_ipython:
        if not show_result:
            display.display(plt.gcf())
            display.clear_output(wait=True)
        else:
            display.display(plt.gcf())
            
            

################# Minor Training Loop
def optimize_model(state, action, next_state, reward): # GPT!!!!!
    # Compute Q(s, a)
    state_action_value = policy_net(state).gather(1, action)

    # Compute target value using policy network
    with torch.no_grad():
        if next_state is None:
            target_value = reward
        else:
            target_value = reward + GAMMA * policy_net(next_state).max(1).values

    # Compute loss and backpropagate
    criterion = nn.SmoothL1Loss()
    loss = criterion(state_action_value, target_value.unsqueeze(1))
    
    optimizer.zero_grad()
    
    loss.backward()
    
    torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100)
    
    optimizer.step()
    
    


#####CREATE GAME
def game(player_sum, dealer_sum, action): 
    
    dealers_turn = False
    
    ##Player's turn to play
    if str(action)== "tensor([[1]])":

        player_sum += value(randint(1, 13)) #new card
        
        if (player_sum <= 21): ##still in play  
            return (player_sum, dealer_sum) , 0, False, False 
        
        else: ## player looses
            return (player_sum, dealer_sum) , -1, True, False  
    
    while dealer_sum < 17:
        dealer_sum += value(randint(1,13))
    
    done = True
    
    if dealer_sum > 21:         # dealer busts
        reward = 1
        win = True
    elif player_sum > dealer_sum:
        reward = 1
        win = True
    elif player_sum == dealer_sum:
        reward = 0
        win = False
    else:                       # dealer wins
        reward = -1
        win = False

                    
    next_state = (player_sum, dealer_sum)
    
    return next_state, reward, done, win 
    
    

def value (card): ## sets up the value of the cards
    
    if (card == 11) or (card == 12) or (card == 13):
        card = 10
    
    return card





num_episodes = 5000
latest_wins = 0

##training loop 
for i_episode in range(num_episodes):
    
    # for this first version, we do not use the fact that aces could represent a 1 or 11
    
    # sum of the players cards
    player_card_1 = value(randint(1, 13))
    player_card_2 = value(randint(1, 13))
    
    player_sum = player_card_1 + player_card_2 ## sum of the cards
    
    # at the beginning, the dealer only has one card
    dealer_sum = value(randint(1, 13))
    
    state = (player_sum, dealer_sum)    
    
    #### converts the state into tensors
    state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
    ##barely changes anything
    
    
    for t in count():
        
        action = select_action(state) # If 0 then hold, if 1 then hit
        
        next_state, reward, done, win = game(player_sum, dealer_sum, action) ##not perfect 
        
        ##updates the player and dealer's sums
        player_sum, dealer_sum = next_state
        
        
        reward = torch.tensor([reward], device=device)
        

        #### converts the next state into tensors 
        if done:
            next_state_tensor = None ## when game ends, we do not optimize equation because we need the next state! 
        else:  
            next_state_tensor = torch.tensor(next_state, dtype=torch.float32, device=device).unsqueeze(0)
        

        ## trains the model (actualises weights)
        optimize_model(state, action, next_state_tensor, reward)
        
        state = next_state_tensor
        
        ##actualise le graphe + break
        if done:
            if i_episode%25 == 0: 
                episode_durations.append((latest_wins/25)*100)
                latest_wins = 0
                plot_durations()
            elif win:
                latest_wins += 1
               
                
            break

print('Complete')
plot_durations(show_result=True)
plt.ioff()
plt.show()



end = time.time()
length = end - start

# Show the results : this can be altered however you like
print("It took", length, "seconds!")

