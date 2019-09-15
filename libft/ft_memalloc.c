/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memalloc.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/04 18:02:36 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/08 09:01:22 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memalloc(size_t size)
{
	void	*p;

	if (size)
		p = (void *)malloc(size);
	else
		return (NULL);
	if (p)
	{
		ft_bzero(p, size);
		return (p);
	}
	else
		return (NULL);
}
