from catmap import ReactionModel, analyze
model = ReactionModel(setup_file = f'input.mkm')
model.output_variables+=['production_rate', 'free_energy','coverage','rate_control']
model.run()
vm=analyze.VectorMap(model)
vm.plot_variable='rate'
vm.log_scale = True
vm.min = 1e-12
vm.max = 1e-3
fig=vm.plot(save='rate.png')

vm.plot_variable='production_rate'
vm.log_scale = True
vm.min = 1e-12
vm.max = 1e-3
fig=vm.plot(save='prod_rate.png')


