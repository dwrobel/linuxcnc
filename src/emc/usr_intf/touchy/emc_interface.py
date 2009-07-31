# Touchy is Copyright (c) 2009  Chris Radek <chris@timeguy.com>
#
# Touchy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Touchy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.



class emc_control:
        def __init__(self, emc):
                self.emc = emc
                self.emccommand = emc.command()
                self.masked = 0;

        def mask(self):
                # updating toggle button active states dumbly causes spurious events
                self.masked = 1

        def unmask(self):
                self.masked = 0

        def mist_on(self, b):
                if self.masked: return
                self.emccommand.mist(1)

        def mist_off(self, b):
                if self.masked: return
                self.emccommand.mist(0)

        def estop(self, b):
                if self.masked: return
                self.emccommand.state(self.emc.STATE_ESTOP)

        def estop_reset(self, b):
                if self.masked: return
                self.emccommand.state(self.emc.STATE_ESTOP_RESET)

        def machine_off(self, b):
                if self.masked: return
                self.emccommand.state(self.emc.STATE_OFF)

        def machine_on(self, b):
                if self.masked: return
                self.emccommand.state(self.emc.STATE_ON)

        def home_all(self, b):
                if self.masked: return
                self.emccommand.mode(self.emc.MODE_MANUAL)
                self.emccommand.home(-1)

        def unhome_all(self, b):
                if self.masked: return
                self.emccommand.mode(self.emc.MODE_MANUAL)
                self.emccommand.unhome(-1)

        def home_x(self, b):
                if self.masked: return
                self.emccommand.mode(self.emc.MODE_MANUAL)
                self.emccommand.home(0)

        def home_y(self, b):
                if self.masked: return
                self.emccommand.mode(self.emc.MODE_MANUAL)
                self.emccommand.home(1)

        def home_z(self, b):
                if self.masked: return
                self.emccommand.mode(self.emc.MODE_MANUAL)
                self.emccommand.home(2)

        def unhome_x(self, b):
                if self.masked: return
                self.emccommand.mode(self.emc.MODE_MANUAL)
                self.emccommand.unhome(0)

        def unhome_y(self, b):
                if self.masked: return
                self.emccommand.mode(self.emc.MODE_MANUAL)
                self.emccommand.unhome(1)

        def unhome_z(self, b):
                if self.masked: return
                self.emccommand.mode(self.emc.MODE_MANUAL)
                self.emccommand.unhome(2)

        def jogging(self, b):
                if self.masked: return
                self.emccommand.mode(self.emc.MODE_MANUAL)

class emc_status:
        def __init__(self, gtk, emc, dros, error, homes, unhomes, estops, machines):
                self.gtk = gtk
                self.dros = dros
                self.error = error
                self.homes = homes
                self.unhomes = unhomes
                self.estops = estops
                self.machines = machines
                self.emc = emc
                self.emcstat = emc.stat()
                self.emcerror = emc.error_channel()
                self.initted = 0

        def periodic(self):
                self.emcstat.poll()
                # XXX tlo?
                self.dros['xr'].set_text("X:% 9.4f" % (self.emcstat.actual_position[0] - self.emcstat.origin[0]))
                self.dros['yr'].set_text("Y:% 9.4f" % (self.emcstat.actual_position[1] - self.emcstat.origin[1]))
                self.dros['zr'].set_text("Z:% 9.4f" % (self.emcstat.actual_position[2] - self.emcstat.origin[2]))
                self.dros['xa'].set_text("X:% 9.4f" % self.emcstat.actual_position[0])
                self.dros['ya'].set_text("Y:% 9.4f" % self.emcstat.actual_position[1])
                self.dros['za'].set_text("Z:% 9.4f" % self.emcstat.actual_position[2])
                self.dros['xd'].set_text("X:% 9.4f" % self.emcstat.dtg[0])
                self.dros['yd'].set_text("Y:% 9.4f" % self.emcstat.dtg[1])
                self.dros['zd'].set_text("Z:% 9.4f" % self.emcstat.dtg[2])

                for j,name in [(0,'x'), (1,'y'), (2,'z')]:
                        self.homes[name].set_active(self.emcstat.homed[j])
                        self.unhomes[name].set_active(not self.emcstat.homed[j])

                estopped = self.emcstat.task_state == self.emc.STATE_ESTOP
                self.estops['estop'].set_active(estopped)
                self.estops['estop_reset'].set_active(not estopped)

                on = self.emcstat.task_state == self.emc.STATE_ON
                self.machines['on'].set_active(on)
                self.machines['off'].set_active(not on)                        

                e = self.emcerror.poll()
                if e:
                        kind, text = e
                        self.error.set_text(text)

                
