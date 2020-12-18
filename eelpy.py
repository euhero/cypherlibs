
import base64


def b64(data):

	return base64.b64encode(data.encode()).decode()


def element(innerherhtml,element="span",id="",attributes="",onclick="",classname=""):

	onclick = f'onclick="{onclick}"' if onclick != "" else ""
	id = f'id="{id}"' if id != "" else ""
	classname = f'class="{classname}"' if classname != "" else ""

	content = f"""<{element} {attributes} {onclick} {id} {classname}>{innerherhtml}</{element}>"""
	
	return content

def table(table_header,table_data,table_id):

	th = ""

	for i in table_header:
		th += element('th',i)

	td = ""

	for tr in table_data:
		trn = ""
		for i in tr:
			trn += element('td',i)
		td += element('tr',trn)

	content = f"""
	<table style="width:100%" id="{table_id}">
  <tr>
    {th}
  </tr>
  {td}
</table>
"""

	return content


def opentab(tabname, pagerenderer=''):
	return f"opentab(event, '{tabname}', {pagerenderer}, true)"

