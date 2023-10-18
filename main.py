from stable_baselines3.sac import SAC
from citylearn.wrappers import NormalizedObservationWrapper, StableBaselines3Wrapper
from env.py import env

dataset_name = 'baeda_3dem'
env = CityLearnEnv(dataset_name, central_agent=True, simulation_end_time_step=1000)
env = NormalizedObservationWrapper(env)
env = StableBaselines3Wrapper(env)
model = SAC('MlpPolicy', env)
model.learn(total_timesteps=env.time_steps*2)

# evaluate
observations = env.reset()

while not env.done:
    actions, _ = model.predict(observations, deterministic=True)
    observations, _, _, _ = env.step(actions)

kpis = env.evaluate()
kpis = kpis.pivot(index='cost_function', columns='name', values='value')
kpis = kpis.dropna(how='all')
display(kpis)
