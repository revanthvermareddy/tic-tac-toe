# tic-tac-toe
AI based tic-tac-toe game challenger. It says "u can't defeate me" :P but if u can, then u can go for a challenge ;)

# Learnings

1. **Reinforcement learning** - This is a very intresting and easy approach where a decision is initially made and by analysing the impact on the **ENVIRONMENT** with the **ACTION** performed we give a sort of **REWARD** when the new state is favourable and sort of **PUNISH** it when its an unfavourable state.
> When we give it a REWARD the value of the new_state will be modified in such a way so as to favour the new state and when we PUNISH it the value of the new_state will be modified in such a way so as to oppose the new state, this helps the AI in future decision making.

2. **Min Max Algorithm** - A very innovative algo indeed. Unlike above AI solution this algorithm only relies on the current state of the game. It takes its decision by being in the opponents shoes and playing his best moves there by evaluating its best possible move to avoid a future loss.
> It uses the concept of branching at a state and playing all possible steps and then taking the favourable step.
