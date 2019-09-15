/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstmap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/06 13:55:35 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/07 15:48:02 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

t_list	*ft_lstmap(t_list *lst, t_list *(*f)(t_list *elem))
{
	t_list	*a;
	t_list	*b;
	t_list	*c;

	if (!lst || !f)
		return (NULL);
	c = (*f)(lst);
	if (!(a = ft_lstnew(c->content, c->content_size)))
		return (NULL);
	b = a;
	lst = lst->next;
	while (lst)
	{
		c = (*f)(lst);
		if (!(a->next = ft_lstnew(c->content, c->content_size)))
			return (NULL);
		a = a->next;
		lst = lst->next;
	}
	return (b);
}
