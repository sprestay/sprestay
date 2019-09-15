/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/08 11:00:06 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/14 16:31:02 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

t_list				*find_true_list(t_list **head, int fd)
{
	t_list		*tmp;

	tmp = *head;
	while (tmp)
	{
		if ((int)tmp->content_size == fd)
			return (tmp);
		tmp = tmp->next;
	}
	tmp = ft_lstnew("", fd);
	ft_lstadd(head, tmp);
	return (*head);
}

int					push_str(t_list **noda, char **line)
{
	char	*n;
	char	*tmp;
	int		i;
	t_list	*a;

	a = *noda;
	i = 0;
	n = a->content;
	while (n[i] != '\n' && n[i] != '\0')
		i++;
	if (n[i] == '\n')
	{
		RETUNER((*line = ft_strsub(n, 0, i)));
		RETUNER((tmp = ft_strdup(n + i + 1)));
		free(a->content);
		a->content = tmp;
	}
	else
	{
		RETUNER((*line = ft_strdup(a->content)));
		ft_strclr(a->content);
	}
	return (1);
}

int					del_node(t_list **list, t_list *node)
{
	t_list	*tmp;

	if (*list == node)
	{
		tmp = (*list)->next;
		ft_memdel(&(*list)->content);
		ft_memdel((void **)list);
		*list = tmp;
	}
	else
	{
		tmp = *list;
		while (tmp->next != node)
			tmp = tmp->next;
		tmp->next = node->next;
		ft_memdel(&node->content);
		ft_memdel((void **)&node);
	}
	return (0);
}

int					get_next_line(const int fd, char **line)
{
	int						ret;
	char					buf[BUFF_SIZE + 1];
	static t_list			*head;
	char					*tmp;
	t_list					*noda;

	if (line == NULL || fd < 0 || read(fd, buf, 0) < 0 || BUFF_SIZE < 1)
		return (-1);
	RETUNER((noda = find_true_list(&head, fd)));
	while ((ret = read(fd, buf, BUFF_SIZE)))
	{
		buf[ret] = '\0';
		RETUNER((tmp = ft_strjoin(noda->content, buf)));
		free(noda->content);
		noda->content = tmp;
		if (ft_strchr(buf, '\n'))
			return (push_str(&noda, line));
	}
	if (ft_strlen(noda->content))
		return (push_str(&noda, line));
	else
		return (del_node(&head, noda));
}
