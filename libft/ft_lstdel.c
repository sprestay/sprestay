/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstdel.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/05 15:44:51 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/05 18:36:49 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_lstdel(t_list **alst, void (*del)(void *, size_t))
{
	t_list *a;
	t_list *b;

	a = *alst;
	while (a)
	{
		b = a->next;
		del(a->content, a->content_size);
		free(a);
		a = b;
	}
	*alst = NULL;
}
