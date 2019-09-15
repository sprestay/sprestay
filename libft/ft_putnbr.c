/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/05 09:36:40 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/06 14:54:27 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int		correct(int *p)
{
	int		m;

	if (*p == -2147483648)
	{
		*p = *p + 1;
		m = 1;
	}
	else
		m = 0;
	if (*p < 0)
	{
		ft_putchar('-');
		*p = *p * (-1);
	}
	return (m);
}

void			ft_putnbr(int nb)
{
	char	counter[100];
	int		i;
	int		m;
	int		*p;

	p = &nb;
	m = correct(p);
	i = 0;
	if (nb == 0)
		ft_putchar('0');
	while (nb > 0)
	{
		counter[i] = '0' + (nb % 10);
		nb /= 10;
		i = i + 1;
	}
	i--;
	counter[0] = counter[0] + m;
	while (i >= 0)
	{
		ft_putchar(counter[i]);
		i = i - 1;
	}
}
