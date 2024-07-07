up: # Levanta o container
	docker-compose up -d

restart:
	docker-compose restart

attach: # Acessa o terminal do container
	docker-compose exec web bash

fix-perms: # Atualiza as permissões dos diretórios, em caso de erro de permissão
	sudo chown -R $(USER):$(USER) .

logs: # Exibe os logs do container
	docker-compose logs -f

stop: # Para o container
	docker-compose stop

install-apps: # Instala as dependências do projeto
	docker-compose exec web pip install -r requirements.txt

create-admin: # Cria um usuário administrador
	docker-compose exec web python manage.py createsuperuser

shell:
	docker-compose exec web python manage.py shell
