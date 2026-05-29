Import com.atlassian.jira.component.ComponentAccessor
def users = ComponentAccessor.getOfBizDelegator().findAll("User");
def usernames=new ArrayList<String>();
users.each{user ->
usernames.add(user.getString("userName"))
usernames.add(user.getString("createdDate"))
}
return usernames;
