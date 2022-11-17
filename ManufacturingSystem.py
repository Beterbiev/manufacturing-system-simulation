import simpy

env = simpy.Environment()
total_waiting_time = 0.0                                     # tiempo de espera total
total_service_duration = 0.0                                 # duracion de servicio total
end = 0.0                                                    # hora en el que finaliza
file_handler = open('sim.txt', 'w')

class Machine:

    def __init__(self, name, repairman, breakdown_time, time_to_repair):
        self.name = name
        self.repairman = repairman
        self.breakdown_time = breakdown_time
        self.time_to_repair = time_to_repair                        

    def break_machine(self, repairmen, breakdown_time, time_to_repair):
        global env
        self.set_breakdown_time(breakdown_time)
        self.set_time_to_repair(time_to_repair)

        yield env.timeout(breakdown_time)                    # deja transcurrir un tiempo entre uno y otro
        env.process(self.request_repairman(self.name, repairmen))
            
    def request_repairman(self, name, repairmen):
        global total_waiting_time
        global end
        global env

        arrives = env.now                                    # guarda el minuto de descompostura de las maquinas

        file_handler.write('\n---> ' + name + ' se descompone a las ' + str(round(arrives, 2)) + ' horas')

        with repairmen.request() as request:

            yield request

            repair_begins = env.now                           # guarda el minuto cuando comienza a ser reparado
            waiting_time = repair_begins - arrives            # calcula el tiempo que tardo
            total_waiting_time = total_waiting_time + waiting_time # acumula los tiempos de espera

            file_handler.write('\n** ' + name + ' es revisada por el reparador a las ' + str(round(repair_begins, 2)) + ' horas, habiendo esperado ' + str(round(waiting_time, 2)) + ' horas')
            
            yield env.process(self.repair_machine(name))      # invoca el proceso repair

            comes_out = env.now                               # guarda la hora en que termina el proceso repair
            file_handler.write('\n<--- ' + name + ' se pone a funcionar denuevo a las ' + str(round(comes_out, 2)) + ' horas')
            end = comes_out                                   # conserva globalmente la hora final de la simulacion

    def repair_machine(self, machine_name):
        global total_service_duration
        yield env.timeout(self.time_to_repair)
        
        file_handler.write('\n\*/ ' + machine_name + ' es reparada en ' + str(round(self.time_to_repair, 2)) + ' horas')
        total_service_duration = total_service_duration + self.time_to_repair
    
    def set_time_to_repair(self, value):
        self.time_to_repair = value
    
    def set_breakdown_time(self, value):
        self.breakdown_time = value


class ManufacturingSystem:

    def __init__(self, sim_time, num_machines, num_repairmen, breakdown_time, repair_time):

        self.num_machines = num_machines
        self.num_repairmen = num_repairmen
        self.sim_time = sim_time
        
        self.breakdown_time = breakdown_time
        self.repair_time = repair_time
        self.j = num_machines

    def simulate(self):
        global env

        repairmen = simpy.Resource(env, self.num_repairmen)

        machines = [Machine('Maquina %d' % (i+1), repairmen, self.breakdown_time[i], self.repair_time[i])
        for i in range(self.num_machines)]
        
        sorted_breakdown = sorted(machines, key=lambda machine: machine.breakdown_time)
        
        while True:

            if end < self.sim_time:
                for i in range(self.num_machines):
                    env.process(sorted_breakdown[i].break_machine(repairmen, sorted_breakdown[i].breakdown_time, sorted_breakdown[i].time_to_repair))
                    self.j+=1
                    machines[machines.index(sorted_breakdown[i])] = Machine('Maquina %d' % (machines.index(sorted_breakdown[i])+1), repairmen, self.breakdown_time[self.j], self.repair_time[self.j])
            else:
                file_handler.write('\n\nTiempo de espera promedio: ' + str(round(total_waiting_time/self.num_repairmen, 2)) + ' horas')
                file_handler.write('\nDuracion de servicio de reparacion promedio: ' + str(round(total_service_duration/(self.j-self.num_machines), 2)) + ' horas')
                time_broken_machines = total_service_duration + total_waiting_time
                cost_broken_machines = time_broken_machines * 50
                cost_repairmen = (self.sim_time * 10) * self.num_repairmen
                total_cost = cost_broken_machines + cost_repairmen
                file_handler.write('\nCosto total de reparadores: $' + str(round(cost_repairmen, 2)))
                file_handler.write('\nCosto total de maquinas descompuestas: $' + str(round(cost_broken_machines, 2)))
                file_handler.write('\nCosto total: $' + str(round(total_cost, 2)))
                file_handler.close()
                break

            sorted_breakdown = sorted(machines, key=lambda machine: machine.breakdown_time)
            env.run()
            