from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class DCOSProvides(RelationBase):
    # Every unit connecting will get the same information
    scope = scopes.GLOBAL

    # Use some template magic to declare our relation(s)
    @hook('{provides:dcos}-relation-{joined,changed}')
    def changed(self):
        # Signify that the relationship is now available to our principal layer(s)
        self.set_state('{relation_name}.available')

    @hook('{provides:dcos}-relation-{broken,departed}')
    def broken(self):
        # Remove the state that our relationship is now available to our principal layer(s)
        self.remove_state('{relation_name}.available')

    # call this method when passed into methods decorated with
    # @when('{relation}.available')
    # to configure the relation data
    def configure(self):
        relation_info = {
            'hostname': hookenv.unit_get('private-address'),
        }
        self.set_remote(**relation_info)
