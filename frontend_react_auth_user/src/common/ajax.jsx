// AJAX library
import axios from 'axios';

var qs = require('qs');

var sendURLEncodedForm = axios.create({
  timeout: 2000,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  headers: {'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'csrfmiddlewaretoken=' + csrftoken
  },
  withCredentials: true
});

var sendFormData = axios.create({
  timeout: 2000,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  headers: {'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'multipart/form-data;boundary=blaBlabla',
            'Cookie': 'csrfmiddlewaretoken=' + csrftoken
  },
  withCredentials: true
});

var sendDelete = axios.create({
  timeout: 2000,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  headers: {'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'multipart/form-data;boundary=blaBlabla',
            'Cookie': 'csrfmiddlewaretoken=' + csrftoken
  },
  withCredentials: true
});

export {sendFormData}
export {sendURLEncodedForm}
export {sendDelete}
