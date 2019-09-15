/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_list_at.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/06 17:40:22 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/06 19:51:16 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

t_list	*ft_list_at(t_list *begin_list, size_t nbr)
{
	size_t	i;
	t_list	*a;

	i = 1;
	a = begin_list;
	while (i < nbr)
	{
		if (!a)
			return (NULL);
		a = a->next;
		i++;
	}
	return (a);
}
