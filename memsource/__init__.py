#!/usr/bin/env python

"""."""

import json
import os.path
import requests

from memsource import auth
from memsource import exceptions
from memsource.constants import MEMSOURCE_ENDPOINT_V1_URL, MEMSOURCE_ENDPOINT_V2_URL


class Memsource:
    """."""

    def __init__(self, username, password):
        self.auth = auth.Auth(username, password)

    def handle_rest_call(self, url, method="GET", data=None, headers=None, files=None, payload=None):
        """Handle HTTP Rest calls to the API"""

        if not headers:
            headers = {
                "Content-type": "application/json",
            }

        headers.update({"Authorization": "ApiToken %s" % self.auth.token})

        if method == "GET":
            result = requests.get(url, headers=headers, params=payload)
        elif method == "POST":
            result = requests.post(url, headers=headers, json=data, data=files)
        elif method == "DELETE":
            result = requests.delete(url, headers=headers, json=data, params=payload)

        if result.status_code == 400:
            raise exceptions.MemsourceHTTPBadRequestException(result)
        if result.status_code == 401:
            raise exceptions.MemsourceHTTPNotAuthorizedException(result)
        elif result.status_code == 403:
            raise exceptions.MemsourceHTTPForbiddenException(result)
        elif result.status_code == 404:
            raise exceptions.MemsourceHTTPNotFoundException(result)
        elif result.status_code == 405:
            raise exceptions.MemsourceHTTPMethodNotAllowedException(result)

        return result

    # Endpoint: projectTemplates
    #
    def get_templates(self, filters=None):
        """
        List all Memsource templates
        Each paginated response is binded
        to a list and returned
        Return type: list
        """

        url = "%s/projectTemplates" % MEMSOURCE_ENDPOINT_V1_URL

        try:
            templates = self.handle_rest_call(url, "GET").json()["content"]
            total_pages = self.handle_rest_call(url, "GET").json()["totalPages"]
            i = 1
            while i <= total_pages:                
                next_page_url = f"{MEMSOURCE_ENDPOINT_V1_URL}/projects/?pageNumber={i}"
                next_page_templates = self.handle_rest_call(next_page_url, "GET").json()["content"]
                templates.extend(next_page_templates)
                i += 1
            return templates if not filters else [item for item in templates if filters.items() <= item.items()]
        except Exception as exc:
            raise exc

        return templates

    # Endpoint: importSettings
    #
    def get_import_settings(self, filters=None):
        """List all Memsource import settings configuration"""

        url = "%s/importSettings" % MEMSOURCE_ENDPOINT_V1_URL

        try:
            import_settings = self.handle_rest_call(url, "GET").json()["content"]

            return import_settings if not filters else [item for item in import_settings if filters.items() <= item.items()]
        except Exception as exc:
            raise exc

    def get_import_settings_by_id(self, import_setting_id):
        """List a Memsource import settings configuration by its id"""

        url = "%s/importSettings/%s" % (MEMSOURCE_ENDPOINT_V1_URL, import_setting_id)

        try:
            return self.handle_rest_call(url, "GET").json()
        except Exception as exc:
            raise exc

    def create_import_settings(self, name, file_import_settings):
        """Create an import settings configuration"""

        url = "%s/importSettings" % MEMSOURCE_ENDPOINT_V1_URL

        kwargs = {
            "name": name,
            "fileImportSettings": file_import_settings
        }

        try:
            return self.handle_rest_call(url, "POST", data=kwargs).json()
        except Exception as exc:
            raise exc

    def delete_import_settings(self, import_setting_id, do_not_fail_on_404=False):
        """Delete a Memsource import setting configuration by its id"""

        url = "%s/importSettings/%s" % (MEMSOURCE_ENDPOINT_V1_URL, import_setting_id)

        try:
            return self.handle_rest_call(url, "DELETE")
        except exceptions.MemsourceHTTPNotFoundException as exc:
            if do_not_fail_on_404:
                resp = requests.models.Response()
                resp.status_code = 404
                return resp
            raise exc
        except Exception as exc:
            raise exc


    # Endpoint: projects
    #
    def get_projects(self, filters=None):
        """
        List all Memsource projects
        Each paginated response is binded
        to a list and returned
        Return type: list
        """

        url = "%s/projects" % MEMSOURCE_ENDPOINT_V1_URL

        try:
            projects = self.handle_rest_call(url, "GET").json()["content"]
            total_pages = self.handle_rest_call(url, "GET").json()["totalPages"]
            i = 1
            while i <= total_pages:                
                next_page_url = f"{MEMSOURCE_ENDPOINT_V1_URL}/projects/?pageNumber={i}"
                next_page_projects = self.handle_rest_call(next_page_url, "GET").json()["content"]
                projects.extend(next_page_projects)
                i += 1
            return projects if not filters else [item for item in projects if filters.items() <= item.items()]
        except Exception as exc:
            raise exc

    def get_project_by_id(self, project_id):
        """Retrieve Memsource project by its id"""

        url = "%s/projects/%s" % (MEMSOURCE_ENDPOINT_V1_URL, project_id)

        try:
            return self.handle_rest_call(url, "GET").json()
        except Exception as exc:
            raise exc

    def get_project_by_name(self, project_name):
        """Retrieve Memsource project by project name"""

        url = "%s/projects/?name=%s" % (MEMSOURCE_ENDPOINT_V1_URL, project_name)

        try:
            return self.handle_rest_call(url, "GET").json()
        except Exception as exc:
            raise exc

    def delete_project(self, project_id, purge=None, do_not_fail_on_404=False):
        """Delete a Memsource project by its id"""

        url = "%s/projects/%s" % (MEMSOURCE_ENDPOINT_V1_URL, project_id)

        query_param = {'purge': purge} if purge is not None else None

        try:
            return self.handle_rest_call(url, "DELETE", payload=query_param)
        except exceptions.MemsourceHTTPNotFoundException as exc:
            if do_not_fail_on_404:
                resp = requests.models.Response()
                resp.status_code = 404
                return resp
            raise exc
        except Exception as exc:
            raise exc

    def get_jobs(self, project_id, filters=None):
        """List all Memsource jobs attached to a project"""

        url = "%s/projects/%s/jobs" % (MEMSOURCE_ENDPOINT_V2_URL, project_id)

        try:
            jobs = self.handle_rest_call(url, "GET").json()["content"]
            return jobs if not filters else [job for job in jobs if job['targetLang'] in filters["target_langs"]]
        except Exception as exc:
            raise exc

    def get_job_by_id(self, job_id, project_id):
        """Retrieve a Memsource job by its id"""

        url = "%s/projects/%s/jobs/%s" % (MEMSOURCE_ENDPOINT_V1_URL, project_id, job_id)

        try:
            return self.handle_rest_call(url, "GET").json()
        except Exception as exc:
            raise exc

    def get_job_targetfile(self, job_id, project_id):
        """Download job target file."""

        url = "%s/projects/%s/jobs/%s/targetFile" % (MEMSOURCE_ENDPOINT_V1_URL, project_id, job_id)

        try:
            return self.handle_rest_call(url, "GET")
        except Exception as exc:
            raise exc

    def delete_job(self, job_id, project_id, purge=None):
        """Delete a Memsource job by its id"""

        return self.delete_jobs([job_id], project_id, purge)

    def delete_jobs(self, job_ids, project_id, purge=None, do_not_fail_on_404=False):
        """Delete a Memsource job by its id"""

        url = "%s/projects/%s/jobs/batch" % (MEMSOURCE_ENDPOINT_V1_URL, project_id)

        query_param = {'purge': purge} if purge is not None else None

        if not isinstance(job_ids, list):
            job_ids = list(job_ids)

        kwargs = {'jobs': [{'uid': job} for job in job_ids]}

        try:
            return self.handle_rest_call(url, "DELETE", payload=query_param, data=kwargs)
        except exceptions.MemsourceHTTPNotFoundException as exc:
            if do_not_fail_on_404:
                resp = requests.models.Response()
                resp.status_code = 404
                return resp
            raise exc
        except Exception as exc:
            raise exc

    def create_project_from_template(self, name, template_id, **kwargs):
        """Create a Memsource project from an existing template."""

        url = "%s/projects/applyTemplate/%s" % (MEMSOURCE_ENDPOINT_V2_URL, template_id)

        try:
            kwargs.update({"name": name})
            return self.handle_rest_call(url, "POST", data=kwargs).json()
        except Exception as exc:
            raise exc

    def create_job(self, project_id, langs, filename, split_filename=None, preTranslate=True, **kwargs):
        """
        Create a Memsource job for a given project and lang.
        Function runs a post request with no 
        Content-type header to post binary files to the 
        server.
        """

        url = "%s/projects/%s/jobs" % (MEMSOURCE_ENDPOINT_V1_URL, project_id)

        kwargs.update({
                    'targetLangs': langs,
                    'preTranslate': preTranslate
        })

        with open(filename, 'rb') as f:
            files = f.read()

        if split_filename:
            kwargs.update({'path': os.path.dirname(filename)})
            _filename = os.path.basename(filename)
        else:
            _filename = filename

        headers = {
            'Content-Disposition': 'filename=' + _filename,
            'Memsource': json.dumps(kwargs),
        }

        try:
            return self.handle_rest_call(url, "POST", headers=headers, files=files).json()
        except Exception as exc:
            raise exc

    # Endpoint: subDomains
    #
    def get_subdomains(self):
        """List all Memsource subDomains"""

        url = "%s/subDomains" % MEMSOURCE_ENDPOINT_V1_URL

        try:
            return self.handle_rest_call(url, "GET").json()["content"]
        except Exception as exc:
            raise exc
