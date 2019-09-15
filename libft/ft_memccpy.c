/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memccpy.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/04 12:28:19 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/05 16:51:49 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memccpy(void *dest, const void *src, int c, size_t n)
{
	unsigned char	*pd;
	unsigned char	*ps;
	size_t			i;

	i = 0;
	ps = (unsigned char *)src;
	pd = (unsigned char *)dest;
	while (i < n)
	{
		pd[i] = ps[i];
		if (ps[i] == (unsigned char)c)
			return (pd + i + 1);
		i++;
	}
	return (NULL);
}
