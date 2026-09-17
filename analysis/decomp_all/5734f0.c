
int FUN__text__005734f0(short *param_1)

{
  short sVar1;
  short *local_8;
  
  local_8 = param_1;
  do {
    sVar1 = *local_8;
    local_8 = local_8 + 1;
  } while (sVar1 != 0);
  return ((int)local_8 - (int)param_1 >> 1) + -1;
}

