from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes

class DCOSRequires(RelationBase):
    scope = scopes.UNIT

    @hook('{requires:dcos}-relation-{joined,changed}')
    def changed(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.available')

    @hook('{requires:dcos}-relation-{departed,broken}')
    def broken(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.available')

    def services(self):
        services = {}
        for conv in self.conversations():
            service_name = conv.scope.split('/')[0]
            service = services.setdefault(service_name, {
                'service_name': service_name,
                'hosts': [],
            })
            host = conv.get_remote('hostname') or conv.get_remote('private-address')
            if host:
                service['hosts'].append({
                    'hostname': host,
                })
        return [s for s in services.values() if s['hosts']]
