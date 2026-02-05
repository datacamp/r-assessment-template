---
title: Introduction to Docker Assessment Items
output: html_document
description: Ten MultipleChoiceChallenge items aligned to Chapters 1–3 of Introduction to Docker.
---

## Starting a container

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-docker
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You want to run Docker's test image to confirm your setup works. The image prints a short message and then exits.

Which command creates and starts that container?

`@options1`
- `docker pull hello-world`
- `docker images hello-world`
- `docker ps hello-world`
- [`docker run hello-world`]

---

## Interactive shells

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-docker
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You run `docker run ubuntu` expecting a shell prompt, but the container exits immediately without any output.

What change would give you an interactive shell?

`@options1`
- Add the `-d` flag
- [Add the `-it` flags]
- Add the `-p` flag
- Use `docker exec` instead

---

## Detached containers

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-docker
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You start a database container without any flags. Your terminal is now blocked showing database logs, and you can't run other commands.

What would have prevented this?

`@options1`
- Using `docker exec` to start it
- [Adding the `-d` flag]
- Adding the `-it` flag
- Using `docker logs` instead

---

## Listing running containers

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-docker
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You started several containers in detached mode and need to get their container IDs so you can stop them later.

Which command shows you the IDs of running containers?

`@options1`
- [`docker ps`]
- `docker images`
- `docker logs`
- `docker pull`

---

## Stopping a container

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-docker
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You need to stop a container gracefully so the application inside can save its state, then free up the container's name for reuse.

Which sequence accomplishes both goals?

`@options1`
- `docker rm` then `docker stop`
- `docker pause` then `docker kill`
- `docker kill` only
- [`docker stop` then `docker rm`]

---

## Naming containers

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-docker
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your team runs five Postgres containers. When someone reports "the database is slow," you check `docker ps` but only see random IDs like `a3f2b9c1`.

What would have made containers easier to identify?

`@options1`
- Using `--label` at build time
- Using `--tag` at run time
- [Using `--name` at run time]
- Using `-f` with `docker ps`

---

## Filtering docker ps

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-docker
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You have 50 running containers and need to find the one named `db_pipeline_v1`. Scrolling through the full list is too slow.

Which `docker ps` option narrows the output to matching containers?

`@options1`
- The `--name` option at runtime
- [The `-f` option for filtering]
- The `-a` option for history
- The `-d` option for details

---

## Inspecting container logs

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-docker
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A container is running but returning errors to users. You need to see what messages the application printed when it started.

Which command helps debug this?

`@options1`
- `docker exec <id> cat /var/log`
- `docker ps -a <id>`
- [`docker logs <id>`]
- `docker inspect <id>`

---

## Following logs in real time

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-docker
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You're debugging a container that occasionally fails. You want your terminal to show new log lines as they appear so you can catch the error when it happens.

Which approach accomplishes this?

`@options1`
- Run `docker logs` repeatedly
- [Run `docker logs -f <id>`]
- Run `docker exec <id> tail`
- Run `docker ps -f status=running`

---

## Pulling a specific image tag

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-docker
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Your project requires Ubuntu 22.04 specifically, not whatever Docker Hub marks as "latest." You need to specify the exact version when pulling.

What separator goes between the image name and version in `docker pull`?

`@options1`
- A space
- [A colon]
- An at-sign
- A hyphen
