# encoding: utf-8

"""
Copyright (c) 2017, Ernesto Ruge
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


from flask_celery import Celery


class LogErrorsCelery(Celery):
    def init_app(self, app):
        super().init_app(app)
        task_base = self.Task

        class ContextTask(task_base):

            def __call__(self, *_args, **_kwargs):
                from ..extensions import logger
                with app.app_context():
                    def on_failure(exc, task_id, args, kwargs, einfo):
                        self.handle_task_error(exc, task_id, args, kwargs, einfo)
                    setattr(self, 'on_failure', on_failure)

                    def handle_task_error(exc, task_id, args, kwargs, traceback):
                        logger.critical('app', str(exc).strip(), str(traceback).strip())
                    setattr(self, 'handle_task_error', handle_task_error)

                    return task_base.__call__(self, *_args, **_kwargs)

        setattr(ContextTask, 'abstract', True)
        setattr(self, 'Task', ContextTask)
