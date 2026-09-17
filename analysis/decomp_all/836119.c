
char * FUN__text1__00836119(char *param_1,char *param_2)

{
  char *local_8;
  
  for (; *param_1 == ' '; param_1 = param_1 + 1) {
  }
  for (local_8 = param_1; (*local_8 != '\0' && (*local_8 != ' ')); local_8 = local_8 + 1) {
  }
  _strncpy(param_2,param_1,(int)local_8 - (int)param_1);
  param_2[(int)local_8 - (int)param_1] = '\0';
  return local_8;
}

