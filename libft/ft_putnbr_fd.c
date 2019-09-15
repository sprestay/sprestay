/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr_fd.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sprestay <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/05 10:24:16 by sprestay          #+#    #+#             */
/*   Updated: 2019/09/06 14:54:58 by sprestay         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int		correct(int *p, int fd)
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
		ft_putchar_fd('-', fd);
		*p = *p * (-1);
	}
	return (m);
}

void			ft_putnbr_fd(int nb, int fd)
{
	char	counter[100];
	int		i;
	int		m;
	int		*p;

	p = &nb;
	m = correct(p, fd);
	i = 0;
	if (nb == 0)
		ft_putchar_fd('0', fd);
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
		ft_putchar_fd(counter[i], fd);
		i = i - 1;
	}
}
