/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnstr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/04 15:04:29 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/06 09:08:45 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strnstr(const char *big, const char *lit, size_t len)
{
	size_t		i;
	size_t		j;

	i = 0;
	if (lit[0] == '\0')
		return ((char *)big);
	while (big[i] != '\0' && i < len)
	{
		j = 0;
		while (big[i + j] == lit[j] && lit[j] != '\0' && big[i + j] != '\0'
				&& (i + j < len))
			j++;
		if (lit[j] == '\0')
			return ((char *)big + i);
		i++;
	}
	return (NULL);
}
