from datetime import date, datetime, timedelta

class K8s:

    @staticmethod
    def age(creation_timestamp ):
        
        created_date = creation_timestamp
        today = datetime.today().replace(tzinfo=None) #- timedelta(hours=5, minutes=30)
        date_diff = today - created_date.replace(tzinfo=None)

        age = ""

        if(date_diff.days == 0):
            seconds = date_diff.total_seconds()
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            age = '{}h,{}m'.format( int(hours), int(minutes) )
        else:
            age = str(date_diff.days) + ' Days'
        
        return age

    @staticmethod
    def namespaces(namespaces):
        namespace_count = 0
        namespace_html_data = namespace_pdf_data = ""
        for n in namespaces.items:
            namespace_count = namespace_count + 1
            ns_age = K8s.age(n.metadata.creation_timestamp)

            namespace_html_data = namespace_html_data + '<tr><td>' + str(namespace_count) + '</td><td>' + n.metadata.name + '</td><td>' + n.status.phase + '</td><td>' + ns_age + '</td><td><a href="/namespace/' + n.metadata.name + '"target="_blank"><img src="http://www.newdesignfile.com/postpic/2009/02/open-new-window-icon_298522.png" width="20px" /></a></td></tr>'
            namespace_pdf_data = namespace_pdf_data + '<tr><td>' + str(namespace_count) + '</td><td>' + n.metadata.name + '</td><td>' + n.status.phase + '</td><td>' + ns_age + '</td></tr>'
                
        return {
            'namespace_count' : namespace_count,
            'namespace_html_data' : namespace_html_data,
            'namespace_pdf_data' : namespace_pdf_data
        }

    @staticmethod
    def nodes(nodes):

        machines_creation_time = []
        nodes_pdf_data = nodes_html_data = ""
        aws_instance_types = ['a1.','t3.','t3a.','t2.','m5.','m5a.','m4.','c5.','c5n.','c4.','r5.','r5a.','r4.','x1e.','x1.','z1d.','p3.','p2.','g3.','f1.','i3.','i3en.','d2.','h1.']
        node_count = node_mem = node_cpu =  total_cpu = total_mem = masters = workers = 0
        master_machine_type = worker_machine_type = machine_type = master_machine_size = worker_machine_size ='Unknown'
        node_role = 'Worker'
        
        for i in nodes.items:

            memory = i.status.capacity['memory']
            cpu = (i.status.capacity['cpu'])
            
            machines_creation_time.append(i.metadata.creation_timestamp )
            
            if (memory.find('Ki') != -1):
                mem=memory.replace("Ki", "")
                node_mem =  int(mem)/1048576
            elif (memory.find('Mi') != -1):
                mem=memory.replace("Mi", "")
                node_mem =  int(mem)/1024
            elif (memory.find('Gi') != -1):
                mem=memory.replace("Gi", "")
                node_mem =  int(mem)

            if (cpu.find('m') != -1):
                node_cpu = int(cpu.replace("m", "") )/1000
            else:
                node_cpu = int(cpu)
            
            total_cpu = total_cpu +  node_cpu
            total_mem = total_mem +  node_mem

            node_count = node_count + 1
            
            node_size = str(node_cpu) + ' Cpus' + ', ' + str(round(node_mem)) + ' Gi'

            try:
                machine_type = i.metadata.labels['beta.kubernetes.io/instance-type']
                if (machine_type.startswith( 'Standard_' )):
                    provider = 'Azure'
                elif (machine_type.startswith( 'f1-' ) or machine_type.startswith( 'g1-' ) or machine_type.startswith( 'n1-' )):
                    provider = 'Google'
                elif (machine_type.startswith(tuple(aws_instance_types))):
                    provider = 'AWS'
                else:
                    provider = 'Unknown'
            except:
                provider = 'Unknown'

            try:
                node_role = str(i.metadata.labels['kubernetes.io/role'])
                
                if (node_role == 'master'):
                    
                    masters = masters + 1
                    
                    try:
                        master_machine_type = i.metadata.labels['beta.kubernetes.io/instance-type']
                        machine_type = i.metadata.labels['beta.kubernetes.io/instance-type']
                        master_machine_size = str(node_cpu) + 'Cpus' + ', ' + str(round(node_mem)) + 'Gi'

                    except:
                        print("Error occured while fetching instance type")

                elif(node_role == 'node'):
                    
                    workers = workers + 1
                    
                    try:
                        worker_machine_type = i.metadata.labels['beta.kubernetes.io/instance-type']
                        machine_type = i.metadata.labels['beta.kubernetes.io/instance-type']
                        worker_machine_size = str(node_cpu) + 'Cpus' + ', ' + str(round(node_mem)) + 'Gi'

                    except:
                        print("Instance type not found in api call responce")
                else:
                    
                    workers = workers +1
                    
                    try:
                        worker_machine_type = i.metadata.labels['beta.kubernetes.io/instance-type']
                        machine_type = i.metadata.labels['beta.kubernetes.io/instance-type']
                        worker_machine_size = str(node_cpu) + 'Cpus' + ', ' + str(round(node_mem)) + 'Gi'
                    except:
                        print("Instance type not found in api call responce")
            except:
                workers = workers + 1
                try:
                    worker_machine_type = i.metadata.labels['beta.kubernetes.io/instance-type']
                    machine_type = i.metadata.labels['beta.kubernetes.io/instance-type']
                    worker_machine_size = str(node_cpu) + 'Cpus' + ', ' + str(round(node_mem)) + 'Gi'                    
                except:
                    print("Instance type not found in api call responce")
            
            node_age = K8s.age(i.metadata.creation_timestamp)
            
            nodes_html_data = nodes_html_data +  '<tr><td>' + str( node_count ) + '</td><td>' + i.metadata.name + '</td><td>' + node_role + '</td><td>' + machine_type + '</td><td>' + node_size + '</td><td>' + node_age + '</td><td><a href="/node/' + i.metadata.name + '"target="_blank"><img src="http://www.newdesignfile.com/postpic/2009/02/open-new-window-icon_298522.png" width="20px" /></a></td></tr>'

            if (len(i.metadata.name) > 50):
                i.metadata.name = i.metadata.name[:50] + '<br>' + i.metadata.name[50:]

            nodes_pdf_data = nodes_pdf_data + '<tr><td>' + str( node_count ) + '</td><td>' + i.metadata.name + '</td><td>' + node_role + '</td><td>' + machine_type + '</td><td>' + node_size + '</td><td>' + node_age + '</td></tr>'
        
        capacity = str(total_cpu) + ' Cpus' + ', ' + str(round(total_mem)) + ' Gi'
        
        least_timestamp = min(machines_creation_time)
        
        running_since = K8s.age(least_timestamp)

        return {'nodes_pdf_data': nodes_pdf_data,
                'nodes_html_data' : nodes_html_data,
                'capacity': capacity ,
                'total_nodes' : node_count,
                'masters' : masters,
                'workers' : workers,
                'master_machine_type' : master_machine_type,
                'worker_machine_type' : worker_machine_type,
                'master_machine_size' : master_machine_size,
                'worker_machine_size' : worker_machine_size,
                'provider': provider,
                'running_since' : running_since }
    
    @staticmethod
    def pods(pods):
        
        pod_count = 0
        pod_html_data = pod_pdf_data = ""

        for po in pods.items:
            pod_count = pod_count + 1
            pod_age = K8s.age(po.metadata.creation_timestamp)
            no_of_containers = ready_pods = restart_count = 0
            if po.status.container_statuses == None :
                no_of_containers = 0
            else:
                no_of_containers = len(po.status.container_statuses)

            for r in range(no_of_containers):
                
                container_statuses = (po.status.container_statuses[r])
                
                if (container_statuses.ready == True):
                    ready_pods = ready_pods + 1
        
                if (container_statuses.restart_count > 0):
                    restart_count = restart_count + container_statuses.restart_count
            
            pod_html_data = pod_html_data + '<tr><td>' + str(pod_count) + '</td><td>' + po.metadata.name + '</td><td>' + po.metadata.namespace + '</td><td>' + str(ready_pods) + '/' + str(no_of_containers) + '</td><td>' + po.status.phase + '</td><td>' + str(restart_count) + '</td><td>' + pod_age + '</td><td><a href="/pod/' + po.metadata.name + '"target="_blank"><img src="http://www.newdesignfile.com/postpic/2009/02/open-new-window-icon_298522.png" width="20px" /></a></td></tr>'

            if (len(po.metadata.name) > 45):
                po.metadata.name = po.metadata.name[:45] + '<br>' + po.metadata.name[45:]
            
            if (len(po.metadata.namespace) > 40):
                po.metadata.name = po.metadata.namespace[:40] + '<br>' + po.metadata.name[40:]

            pod_pdf_data = pod_pdf_data + '<tr><td>' + str(pod_count) + '</td><td>' + po.metadata.name + '</td><td>' + po.metadata.namespace + '</td><td>' + str(ready_pods) + '/' + str(no_of_containers) + '</td><td>' + po.status.phase + '</td><td>' + str(restart_count) + '</td><td>' + pod_age + '</td></tr>'

        return {
                'pod_html_data' : pod_html_data,
                'pod_pdf_data' : pod_pdf_data,
                'pod_count' : pod_count
               }

    @staticmethod
    def workloads(deployments,daemonsets,statefulsets):
        
        workloads_count = deployments_count = daemonsets_count = statefulsets_count = 0
        workload_html_data = workload_pdf_data = ""

        for dep in deployments.items:
            dep_age = K8s.age(dep.metadata.creation_timestamp)
            workloads_count = workloads_count + 1
            deployments_count = deployments_count + 1

            workload_html_data =  workload_html_data + '<tr><td>' + str(workloads_count) +  '</td><td>Deployment</td><td>' + dep.metadata.name + '</td><td>' + dep.metadata.namespace + '</td><td>' + str(dep.spec.replicas) + '</td><td>' + str(dep.status.ready_replicas) + '</td><td>' + dep_age + '</td><td><a href="/deployment/' + dep.metadata.name + '"target="_blank"><img src="http://www.newdesignfile.com/postpic/2009/02/open-new-window-icon_298522.png" width="20px" /></a></td></tr>'

            if (len(dep.metadata.name) > 45):
                dep.metadata.name = dep.metadata.name[:45] + '<br>' + dep.metadata.name[45:]
            
            if (len(dep.metadata.namespace) > 40):
                dep.metadata.name = dep.metadata.namespace[:40] + '<br>' + dep.metadata.name[40:]
            
            workload_pdf_data = workload_pdf_data + '<tr><td>' + str(workloads_count) +  '</td><td>Deployment</td><td>' + dep.metadata.name + '</td><td>' + dep.metadata.namespace + '</td><td>' + str(dep.spec.replicas) + '</td><td>' + str(dep.status.ready_replicas) + '</td><td>' + dep_age + '</td></tr>'

        for dae in daemonsets.items:
            dae_age = K8s.age(dae.metadata.creation_timestamp)
            workloads_count = workloads_count + 1
            statefulsets_count = statefulsets_count + 1
            
            workload_html_data =  workload_html_data + '<tr><td>' + str(workloads_count) +  '</td><td>Daemonset</td><td>' + dae.metadata.name + '</td><td>' + dae.metadata.namespace + '</td><td>' + str(dae.status.desired_number_scheduled) + '</td><td>' + str((dae.status.number_ready)) + '</td><td>' + dae_age + '</td><td><a href="/daemonset/' + dae.metadata.name + '"target="_blank"><img src="http://www.newdesignfile.com/postpic/2009/02/open-new-window-icon_298522.png" width="20px" /></a></td></tr>'

            if (len(dae.metadata.name) > 45):
                dae.metadata.name = dae.metadata.name[:45] + '<br>' + dae.metadata.name[45:]
            
            if (len(dae.metadata.namespace) > 40):
                dae.metadata.name = dae.metadata.namespace[:40] + '<br>' + dae.metadata.name[40:]

            workload_pdf_data = workload_pdf_data + '<tr><td>' + str(workloads_count) +  '</td><td>Daemonset</td><td>' + dae.metadata.name + '</td><td>' + dae.metadata.namespace + '</td><td>' + str(dae.status.desired_number_scheduled) + '</td><td>' + str((dae.status.number_ready)) + '</td><td>' + dae_age + '</td></tr>'

        for st in statefulsets.items:
            st_age = K8s.age(st.metadata.creation_timestamp)
            workloads_count = workloads_count + 1
            daemonsets_count = daemonsets_count + 1

            workload_html_data =  workload_html_data = '<tr><td>' + str(workloads_count) +  '</td><td>Statefulset</td><td>' + st.metadata.name + '</td><td>' + st.metadata.namespace + '</td><td>' + str(st.spec.replicas) + '</td><td>' + str(st.status.ready_replicas) + '</td><td>' + st_age + '</td><td><a href="/statefulset/' + st.metadata.name + '"target="_blank"><img src="http://www.newdesignfile.com/postpic/2009/02/open-new-window-icon_298522.png" width="20px" /></a></td></tr>'

            if (len(st.metadata.name) > 45):
                st.metadata.name = st.metadata.name[:45] + '<br>' + st.metadata.name[45:]
            
            if (len(st.metadata.namespace) > 40):
                st.metadata.name = st.metadata.namespace[:40] + '<br>' + st.metadata.name[40:]            

            workload_pdf_data = workload_pdf_data + '<tr><td>' + str(workloads_count) +  '</td><td>Statefulset</td><td>' + st.metadata.name + '</td><td>' + st.metadata.namespace + '</td><td>' + str(st.spec.replicas) + '</td><td>' + str(st.status.ready_replicas) + '</td><td>' + st_age + '</td></tr>'
        
        return {
            'workload_html_data' : workload_html_data,
            'workload_pdf_data' : workload_pdf_data,
            'deployments_count' : deployments_count,
            'daemonsets_count' : daemonsets_count,
            'statefulsets_count' : statefulsets_count
            }
 
    @staticmethod
    def services(services):
        service_count = 0
        service_html_data = service_pdf_data = ""

        for svc in services.items:
            
            service_count = service_count + 1
            svc_age = K8s.age(svc.metadata.creation_timestamp)

            service_ports  = ""
            no_of_ports = len(svc.spec.ports)

            for j in range(no_of_ports): 
            
                ports_data = (svc.spec.ports[j])
            
                service_port = str(ports_data.port) + '/' + ports_data.protocol

                if (j > 0):
                    service_ports = service_ports + '<br>'
            
                service_ports = service_ports + str (service_port)

            if (svc.spec.type == 'LoadBalancer'):
                
                try:
                    ingress = svc.status.load_balancer.ingress[0]
                
                    if (ingress.ip == None):
                        service_endpoints = "<a href='http://" + ingress.hostname + "' target='_top'>Click here</a>"
                        #service_endpoints = ingress.hostname
                    else:
                        service_endpoints = "<a href='http://" + ingress.ip + "' target='_top'>Click here</a>"
                        #service_endpoints = ingress.ip
                except:
                    service_endpoints = "Pending"    
            else:
                service_endpoints = 'None'

            service_html_data  =  service_html_data + '<tr><td>' + str(service_count) + '</td><td>' + svc.metadata.name + '</td><td>' + svc.metadata.namespace + '</td><td>' + svc.spec.type + '</td><td>' + service_ports + '</td><td>'+ service_endpoints + '</td><td>' + svc_age +  '</td><td><a href="/service/' + svc.metadata.name + '"target="_blank"><img src="http://www.newdesignfile.com/postpic/2009/02/open-new-window-icon_298522.png" width="20px" /></a></td></tr>'

            if (len(svc.metadata.name) > 45):
                svc.metadata.name = svc.metadata.name[:45] + '<br>' + svc.metadata.name[45:]
            
            if (len(svc.metadata.namespace) > 40):
                svc.metadata.name = svc.metadata.namespace[:40] + '<br>' + svc.metadata.name[40:]
            
            service_pdf_data  =  service_pdf_data + '<tr><td>' + str(service_count) + '</td><td>' + svc.metadata.name + '</td><td>' + svc.metadata.namespace + '</td><td>' + svc.spec.type + '</td><td>' + service_ports + '</td><td>'+ service_endpoints + '</td><td>' + svc_age +  '</td></tr>'
        
        return{
            'service_html_data' : service_html_data,
            'service_pdf_data' : service_pdf_data,
            'service_count' : service_count
        }
    
    @staticmethod
    def ingress(ingress):
        
        ingress_count = 0
        ingress_html_data = ingress_pdf_data = applications_html_data = ""

        for ing in ingress.items:
            
            ingress_count = ingress_count + 1
            ing_age = K8s.age(ing.metadata.creation_timestamp)
            hosts = service_name = service_port = path = ""
            
            # Ignore cert-manager acme http-solver
            if ( "cm-acme-http-solver" in ing.metadata.name ):
                continue

            no_of_hosts = len(ing.spec.rules)

            for j in range(no_of_hosts): 
            
                rule_data = (ing.spec.rules[j])

                host_data ='<a href="http://' + rule_data.host + '"target="_top">Click here</a>'
                
                if (j > 0):
                    hosts = hosts + '<br>'
            
                hosts = hosts + host_data
                
                no_of_paths = len(rule_data.http.paths)
                
                for k in range(no_of_paths):
                    if ( k > 0 ):
                        service_name = service_name + '<br>'
                        service_port = service_port + '<br>'
                        path =  path + '<br>'

                    path_data = rule_data.http.paths[k]
                    service_name =  service_name + path_data.backend.service_name
                    service_port =  service_port + str(path_data.backend.service_port)
                    path =  path + path_data.path
            
            ingress_html_data =  ingress_html_data + '<tr><td>' + str( ingress_count )+ '</td><td>' + ing.metadata.name + '</td><td>' + ing.metadata.namespace + '</td><td>' + service_name + '</td><td>' + str(service_port) + '</td><td>' + path + '</td><td>' + hosts + '</td><td>' +  ing_age + '</td><td><a href="/ingress/' + ing.metadata.name + '"target="_blank"><img src="http://www.newdesignfile.com/postpic/2009/02/open-new-window-icon_298522.png" width="20px" /></a></td></tr>'

            if (len(ing.metadata.name) > 30):
                ing.metadata.name = ing.metadata.name[:30] + '<br>' + ing.metadata.name[30:]
            
            if (len(ing.metadata.namespace) > 25):
                ing.metadata.name = ing.metadata.namespace[:25] + '<br>' + ing.metadata.name[25:]
            
            ingress_pdf_data =  ingress_pdf_data + '<tr><td>' + str( ingress_count )+ '</td><td>' + ing.metadata.name + '</td><td>' + ing.metadata.namespace + '</td><td>' + service_name + '</td><td>' + path + '</td><td>' + hosts + '</td><td>' +  ing_age + '</td></tr>'

            applications_html_data =  applications_html_data + '<tr><td>' + str( ingress_count )+ '</td><td>' +  ing.metadata.namespace +  '</td><td>' + ing.metadata.name +  '</td><td>' + hosts + '</td><td>' +  ing_age + '</td><td><a href="/application"target="_blank"><img src="http://www.newdesignfile.com/postpic/2009/02/open-new-window-icon_298522.png" width="20px" /></a></td></tr>'

        return {
            'ingress_html_data' : ingress_html_data,
            'ingress_pdf_data' : ingress_pdf_data,
            'applications_html_data' : applications_html_data,
            'ingress_count' : ingress_count
        }

    @staticmethod
    def volumes(pv):
        pv_count = 0
        pv_html_data = pv_pdf_data = ""
        
        for p in pv.items:
            pv_count = pv_count + 1
            pv_age = K8s.age(p.metadata.creation_timestamp)

            pv_html_data = pv_html_data + '<tr><td>' + str (pv_count) + '</td><td>' + p.metadata.name + '</td><td>' + p.spec.storage_class_name + '</td><td>' + p.spec.capacity['storage'] + '</td><td>' +  p.spec.claim_ref.name + '</td><td>' + pv_age + '</td><td><a href="/volume/' + p.metadata.name + '"target="_blank"><img src="http://www.newdesignfile.com/postpic/2009/02/open-new-window-icon_298522.png" width="20px" /></a></td></tr>'
            
            if (len(p.spec.claim_ref.name) > 40):
                p.spec.claim_ref.name = p.spec.claim_ref.name[:40] + '<br>' + p.spec.claim_ref.name[40:]

            pv_pdf_data = pv_pdf_data + '<tr><td>' + str (pv_count) + '</td><td>' + p.metadata.name + '</td><td>' + p.spec.storage_class_name + '</td><td>' + p.spec.capacity['storage'] + '</td><td>' +  p.spec.claim_ref.name + '</td><td>' + pv_age + '</td></tr>'

        return {
            'pv_html_data' : pv_html_data,
            'pv_pdf_data' : pv_pdf_data,
            'pv_count' : pv_count
        }
