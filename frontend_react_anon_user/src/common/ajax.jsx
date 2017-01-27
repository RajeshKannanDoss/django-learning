// AJAX library
import axios from 'axios';

var instance = axios.create({
  timeout: 3500,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  headers: {'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'csrfmiddlewaretoken=' + csrftoken
  },
  withCredentials: true
});

export {instance}
