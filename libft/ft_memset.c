/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memset.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/04 08:53:05 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/08 09:30:25 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memset(void *dest, int c, size_t n)
{
	size_t i;

	i = 0;
	if (n < n + 1)
	{
		while (i < n)
		{
			*((unsigned char *)dest + i) = (unsigned char)c;
			i++;
		}
	}
	else
	{
		while (i < n - 1)
		{
			*((unsigned char *)dest + i) = (unsigned char)c;
			i++;
		}
		*((unsigned char *)dest + i) = (unsigned char)c;
	}
	return (dest);
}
