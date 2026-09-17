
int __thiscall FUN__text1__0080eb87(undefined4 *param_1,void *param_2,void *param_3)

{
  void *pvVar1;
  bool bVar2;
  int local_8;
  
  pvVar1 = param_2;
  bVar2 = param_3 < param_2;
  if (bVar2) {
    param_2 = param_3;
    param_3 = pvVar1;
  }
  local_8 = _memcmp(param_2,param_3,param_1[1] - (int)param_3);
  if (local_8 == 0) {
    param_2 = (void *)((int)param_2 + (param_1[1] - (int)param_3));
    param_3 = (void *)*param_1;
    local_8 = _memcmp(param_2,param_3,param_1[1] - (int)param_2);
  }
  if (local_8 == 0) {
    local_8 = _memcmp((void *)*param_1,(void *)((int)param_3 + (param_1[1] - (int)param_2)),
                      (int)pvVar1 - (int)*param_1);
  }
  if (bVar2) {
    local_8 = -local_8;
  }
  return local_8;
}

