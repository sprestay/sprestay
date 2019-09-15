/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bzero.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/04 10:05:02 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/08 09:38:47 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_bzero(void *s, size_t n)
{
	size_t i;

	i = 0;
	if (n < n + 1)
	{
		while (i < n)
		{
			*((unsigned char *)s + i) = 0;
			i++;
		}
	}
	else
	{
		while (i < n - 1)
		{
			*((unsigned char *)s + i) = 0;
			i++;
		}
		*((unsigned char *)s + i) = 0;
	}
}
