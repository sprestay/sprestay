/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_l_strsplit.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/06 16:23:47 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/08 08:47:47 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

t_list		*ft_l_strsplit(char const *s, char c)
{
	int		i;
	char	**ar;
	t_list	*begin;
	t_list	*a;

	i = 1;
	if (!s)
		return (NULL);
	ar = ft_strsplit(s, c);
	begin = ft_lstnew(ar[0], (ft_strlen(ar[0]) + 1));
	a = begin;
	while (ar[i] != '\0')
	{
		a->next = ft_lstnew(ar[i], (ft_strlen(ar[i]) + 1));
		a = a->next;
		i++;
	}
	return (begin);
}
