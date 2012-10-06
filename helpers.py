from coffin.shortcuts import render_to_response, render_to_string
from bars.settings import DEBUG#, GOOGLE_ANALYTICS
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from functools import wraps

def render(html_template=False, json_template=False):
  """
  Render an html response by default
  or a json response only for ajax requests
  """
  def render_json(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
      try:
        context = view_func(request, *args, **kwargs)
        if not context:
          raise Exception('No context generated')
        
        # Skip render on redirect
        if isinstance(context, HttpResponseRedirect):
          return context

        # Add some settings to context
        context['DEBUG'] = DEBUG
        context['IS_AJAX'] = request.is_ajax()
        #context['GOOGLE_ANALYTICS'] = GOOGLE_ANALYTICS

        # Ajax render using json
        if request.is_ajax() and json_template:
          
          # Render the template to html
          html = render_to_string(json_template, context)
          json_data = {
            'status' : 'ok',
            'html' : html,
          }
          
          resp = HttpResponse(mimetype='application/json')
          resp.write(simplejson.dumps(json_data))
            
        # Html render
        elif html_template:
          resp = render_to_response(
            html_template,
            context,
            context_instance=RequestContext(request),
          )
          
        else:
          raise Exception('No template found')
        
      except Exception, e:
        if DEBUG:
          raise
        if request.is_ajax():
          json_data = {'status' : 'error', 'message' : str(e)}
          resp = HttpResponse(mimetype='application/json')
          resp.write(simplejson.dumps(json_data))
        else:
          resp = render_to_response(
            'error.html',
            {'error' : str(e),},
          )
      
      return resp

    return wrapper
  return render_json

def nameize(s, max = 40):
  import re, unicodedata

  # Remove all accents
  try:
    s = unicode(s, 'ISO-8859-1')
  except:
    pass
  s = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore')

  # Remove all non allowed chars
  s = re.sub('[^a-z0-9 ]', '', s.strip().lower(),)

  # Remove multiple spaces
  s = re.sub('[ ]+', ' ', s.strip().lower(),)

  # Limit words to match chars length
  words = s.split(' ')
  cpt = 0
  nb = 0
  for w in words:
    cpt += len(w)
    if cpt > max:
      break
    nb += 1
  s = '_'.join(words[0:nb])

  return s