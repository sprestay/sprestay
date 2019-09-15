/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/04 12:40:37 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/06 15:56:55 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memmove(void *dest, const void *src, size_t n)
{
	size_t			i;
	unsigned char	*pd;
	unsigned char	*ps;

	pd = (unsigned char *)dest;
	ps = (unsigned char *)src;
	if (!pd && !ps)
		return (dest);
	i = 0;
	if (ps >= pd)
		while (i < n)
		{
			pd[i] = ps[i];
			i++;
		}
	else
		while (n)
		{
			pd[n - 1] = ps[n - 1];
			n--;
		}
	return (dest);
}
