from appuifw import *
from e32 import ao_sleep,Ao_lock
from sysagent2 import *
#from esysagent import *


def viewsysagent():
  app.body.clear()
  status=get_sim_status()
  text="SIM Status = %d"%status
  app.body.add(u'%s\n'%text)
   
  status=get_network_status()
  text="Network Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_network_strength()
  text="Network Strength = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_inbox_status()
  text="Inbox Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_outbox_status()
  text="Outbox Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_irda_status()
  text="irda Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_network_bars()
  text="network bars = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_gprs_availability()
  text="gprs availability = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_gprs_status()
  text="gprs Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_silent_mode()
  text="silent mode = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_call_forwarding_status()
  text="Call forwarding Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_voice_mail_status()
  text="Voice mail Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_sim_sms_memory_status()
  text="irda Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_sim_ready_status()
  text="SIM ready Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_sim_card_status()
  text="SIM card Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_sim_changed_status()
  text="SIM changed Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_home_zone_status()
  text="home zone Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_fax_message_status()
  text="fax message Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_fax_message_status()
  text="fax message Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_email_message_status()
  text="email message Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_other_message_status()
  text="other_message Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=gget_security_code_status()
  text="security_code Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_autolock_status()
  text="autolock Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_simlock_status()
  text="simlock Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_first_boot_status()
  text="first boot Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_sim_owned_status()
  text="sim owned Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_new_email_status()
  text="new email Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_wcdma_status()
  text="wcdma Status = %d"%status
  app.body.add(u'%s\n'%text)

  status=get_sim_present()
  text="sim present = %d"%status
  app.body.add(u'%s\n'%text)


lock=Ao_lock()
app.body=Text()
app.body.clear()
app.exit_key_handler=lock.signal
app.menu = [(u"View sysagent info",viewsysagent)]
lock.wait()
