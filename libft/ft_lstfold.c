/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstfold.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/06 19:56:42 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/08 08:48:49 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_lstfold(t_list *list, void *(*f)(void *d, void *s))
{
	void	*s;

	if (!list || !f)
		return (NULL);
	s = list->content;
	list = list->next;
	while (list)
	{
		s = (*f)(s, list->content);
		list = list->next;
	}
	return (s);
}
