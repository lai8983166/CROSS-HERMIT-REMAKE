
/* Library Function - Single Match
    __IncMan
   
   Library: Visual Studio */

int __IncMan(int param_1,int param_2)

{
  int local_14;
  int local_10;
  
  local_10 = (int)(param_2 + (param_2 >> 0x1f & 0x1fU)) >> 5;
  local_14 = ___addl(*(undefined4 *)(param_1 + local_10 * 4),
                     1 << (0x1f - ((byte)param_2 & 0x1f) & 0x1f),param_1 + local_10 * 4);
  while ((local_10 = local_10 + -1, -1 < local_10 && (local_14 != 0))) {
    local_14 = ___addl(*(undefined4 *)(param_1 + local_10 * 4),1,param_1 + local_10 * 4);
  }
  return local_14;
}

