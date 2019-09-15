/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstnew.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/05 10:59:00 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/05 11:20:49 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

t_list	*ft_lstnew(void const *content, size_t content_size)
{
	t_list	*a;

	a = NULL;
	a = (t_list *)malloc(sizeof(t_list));
	if (a)
	{
		if (!content)
		{
			a->content = NULL;
			a->content_size = 0;
			a->next = NULL;
		}
		else
		{
			a->content = malloc(content_size);
			if (!a)
				return (NULL);
			a->content = ft_memcpy(a->content, content, content_size);
			a->content_size = content_size;
			a->next = NULL;
		}
	}
	return (a);
}
